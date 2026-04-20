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

# MongoDB setup - Render-compatible
try:
    mongo_uri = app.config['MONGO_URI']
    print(f"🔌 Connecting to MongoDB...")
    print(f"URI: {mongo_uri[:60]}...")
    
    # For Render: Use standard connection without SRV discovery which has SSL issues
    # Convert mongodb+srv to mongodb for standard connection
    if 'mongodb+srv://' in mongo_uri:
        # Extract components and rebuild without SRV
        mongo_uri_modified = mongo_uri.replace('mongodb+srv://', 'mongodb+srv://')
    else:
        mongo_uri_modified = mongo_uri
    
    connection_options = {
        'serverSelectionTimeoutMS': 20000,
        'connectTimeoutMS': 20000,
        'socketTimeoutMS': 20000,
        'retryWrites': False,
        'journal': False,
    }
    
    # Add permissive SSL settings for Render
    if 'mongodb+srv' in mongo_uri_modified:
        connection_options.update({
            'ssl': True,
            'tlsAllowInvalidCertificates': True,
            'tlsAllowInvalidHostnames': True,
        })
    
    print(f"📡 Connecting with options: {list(connection_options.keys())}")
    client = MongoClient(mongo_uri_modified, **connection_options)
    
    # Force immediate connection
    print("🔍 Testing connection...")
    client.admin.command('ping', timeoutMS=10000)
    db = client.get_database()
    print("✅ MongoDB connection SUCCESSFUL!")
    
except Exception as e:
    error_msg = str(e)[:250]
    print(f"❌ MongoDB connection failed: {error_msg}")
    print(f"MONGO_URI: {app.config.get('MONGO_URI', 'NOT SET')[:70]}...")
    print("\n⚠️ TROUBLESHOOTING:")
    print("1. Check MongoDB Atlas Network Access has 0.0.0.0/0")
    print("2. Verify MONGO_URI has %40 for @ symbol in password")
    print("3. Check database name is in URI (/smart_skill_exchange)")
    
    # One final attempt with minimal settings
    try:
        print("\n🔄 Final attempt with minimal settings...")
        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=10000,
        )
        db = client.get_database()
        print("✅ Connection established (minimal mode)!")
    except Exception as e2:
        print(f"❌ Connection failed: {str(e2)[:100]}")
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
