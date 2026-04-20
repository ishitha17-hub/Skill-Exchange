import sys
import os
import ssl
import certifi

# Ensure this backend directory is always on sys.path so that
# imports like 'utils', 'models', 'routes', 'config' resolve correctly
# regardless of which working directory the app is launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, redirect, url_for
from config import Config
from pymongo import MongoClient
from flask_login import LoginManager
from models.user import User
from models.admin import Admin

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config.from_object(Config)

# MongoDB setup with proper SSL handling
try:
    mongo_uri = app.config['MONGO_URI']
    print(f"Connecting to MongoDB with URI: {mongo_uri[:50]}...")
    
    connection_options = {
        'serverSelectionTimeoutMS': 15000,
        'connectTimeoutMS': 15000,
        'socketTimeoutMS': 15000,
        'retryWrites': False,
    }
    
    # For mongodb+srv (Atlas), add proper SSL options
    if 'mongodb+srv' in mongo_uri:
        connection_options.update({
            'ssl': True,
            'tlsAllowInvalidCertificates': True,
            'tlsAllowInvalidHostnames': True,
            'tlsCAFile': certifi.where(),
        })
    
    print(f"Attempting connection to MongoDB...")
    client = MongoClient(mongo_uri, **connection_options)
    
    # Force connection test
    db = client.get_database()
    print("✅ Attempting ping...")
    client.admin.command('ping', timeoutMS=5000)
    print("✅ MongoDB connection SUCCESSFUL!")
    
except Exception as e:
    error_msg = str(e)[:300]
    print(f"❌ MongoDB connection failed: {error_msg}")
    print(f"MONGO_URI: {app.config.get('MONGO_URI', 'NOT SET')[:60]}...")
    
    # Try minimal fallback with relaxed settings
    try:
        print("\n🔄 Attempting fallback connection...")
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=8000,
            connectTimeoutMS=8000,
            retryWrites=False,
            ssl=True,
            tlsAllowInvalidCertificates=True,
            tlsAllowInvalidHostnames=True,
        )
        db = client.get_database()
        client.admin.command('ping', timeoutMS=3000)
        print("✅ Fallback connection SUCCESSFUL!")
    except Exception as e2:
        print(f"❌ Fallback failed: {str(e2)[:200]}")
        print("Check: 1) MONGO_URI is correct")
        print("       2) MongoDB Atlas IP whitelist includes 0.0.0.0/0")
        print("       3) Network access is allowed from Render region")
        sys.exit(1)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.get_by_id(db, user_id)
    if user: return user
    admin = Admin.get_by_id(db, user_id)
    if admin: return admin
    return None

# Register Blueprints
from routes.auth_routes import create_auth_blueprint
from routes.user_routes import create_user_blueprint
from routes.admin_routes import create_admin_blueprint
from routes.course_routes import create_course_blueprint

app.register_blueprint(create_auth_blueprint(db))
app.register_blueprint(create_user_blueprint(db))
app.register_blueprint(create_admin_blueprint(db))
app.register_blueprint(create_course_blueprint(db))

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5005))
    # Use debug=False in production (when PORT is set by hosting provider)
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, port=port, host='0.0.0.0')
