from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt

class User:
    def __init__(self, db):
        self.collection = db['users']

    def create_user(self, username, role, password, public_key=None):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'username': username,
            'role': role,
            'password': hashed_password,
            'public_key': public_key,
            'has_voted': False
        }
        return self.collection.insert_one(user_data)
    
    def find_user_by_username(self, username):
        return self.collection.find_one({"username": username})
    
    def find_user_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})

    def update_user(self, user_id, data):
        self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
