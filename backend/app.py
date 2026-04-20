import sys
import os
import ssl

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

# MongoDB setup
try:
    mongo_uri = app.config['MONGO_URI']
    print(f"Connecting to MongoDB with URI: {mongo_uri[:50]}...")
    
    # Build connection options
    connection_options = {
        'serverSelectionTimeoutMS': 10000,
        'connectTimeoutMS': 10000,
        'socketTimeoutMS': 10000,
        'retryWrites': True,
    }
    
    # For Render environment, handle SSL specially
    if 'mongodb+srv' in mongo_uri:
        connection_options.update({
            'ssl': True,
            'ssl_cert_reqs': 'CERT_NONE',  # For Render SSL issues
            'tlsAllowInvalidCertificates': True,
        })
    
    client = MongoClient(mongo_uri, **connection_options)
    db = client.get_database()
    
    # Verify connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
except Exception as e:
    print(f"❌ MongoDB connection failed: {str(e)[:200]}")
    print(f"MONGO_URI from config: {app.config.get('MONGO_URI', 'NOT SET')[:50]}...")
    print("Retrying with alternative settings...")
    try:
        # Fallback: Try with even more relaxed SSL settings
        client = MongoClient(mongo_uri, retryWrites=False, serverSelectionTimeoutMS=5000)
        db = client.get_database()
        client.admin.command('ping')
        print("✅ MongoDB connection successful (fallback)!")
    except Exception as e2:
        print(f"❌ Final attempt failed: {str(e2)[:200]}")
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
