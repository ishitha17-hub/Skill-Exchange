from flask_login import UserMixin
from bson.objectid import ObjectId

class Admin(UserMixin):
    def __init__(self, admin_data):
        self.id = str(admin_data.get('_id'))
        self.email = admin_data.get('email')
        self.name = admin_data.get('name', 'Admin')
        self.password_hash = admin_data.get('password_hash')
        self.role = admin_data.get('role', 'admin')

    @staticmethod
    def get_by_id(db, admin_id):
        try:
            admin_data = db.admins.find_one({'_id': ObjectId(admin_id)})
            if admin_data:
                return Admin(admin_data)
        except Exception:
            return None
        return None

    @staticmethod
    def get_by_email(db, email):
        admin_data = db.admins.find_one({'email': email})
        if admin_data:
            return Admin(admin_data)
        return None
