import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-change-in-production'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/smart_skill_exchange'
    # Add SSL/TLS options for cloud MongoDB
    if 'mongodb+srv' in (os.environ.get('MONGO_URI') or ''):
        MONGO_URI += '&ssl=true&retryWrites=true&w=majority'

