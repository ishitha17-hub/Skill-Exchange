from flask_login import UserMixin
from bson.objectid import ObjectId
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get('_id'))
        self.name = user_data.get('name')
        self.email = user_data.get('email')
        self.password_hash = user_data.get('password_hash')
        self.skills_interests = user_data.get('skills_interests', [])
        # Useful to distinguish between User and Admin in templates/routes if needed
        self.role = user_data.get('role', 'user')
        self.is_suspended = user_data.get('is_suspended', False)

    @staticmethod
    def get_by_id(db, user_id):
        try:
            user_data = db.users.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return User(user_data)
        except Exception:
            return None
        return None

    @staticmethod
    def get_by_email(db, email):
        user_data = db.users.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None
