from pymongo import MongoClient
import os
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId

def setup():
    print("Setting up MongoDB database: smart_skill_exchange")
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client.smart_skill_exchange

    # Create collections implicitly by inserting dummy data if needed, but not required
    # Let's just create the admin user
    
    admin_email = "admin@skill-exchange.com"
    admin_password = "adminpassword123"
    
    existing_admin = db.admins.find_one({"email": admin_email})
    
    if existing_admin:
        print(f"Admin account already exists: {admin_email}")
    else:
        admin_data = {
            "email": admin_email,
            "password_hash": generate_password_hash(admin_password),
            "role": "admin"
        }
        db.admins.insert_one(admin_data)
        print(f"Admin account created successfully!")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        
    print("\nDatabase configuration complete. You can now start the application.")

if __name__ == "__main__":
    setup()
