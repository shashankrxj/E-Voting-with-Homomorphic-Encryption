from flask import request, jsonify
import bcrypt
import jwt
import datetime
from models.user_model import User
from db import get_db

db = get_db()
user_model = User(db)

SECRET_KEY = "your_jwt_secret"

def register():
    data = request.json
    username = data['username']
    role = data['role']
    password = data['password']
    public_key = data.get('public_key', None)

    if user_model.find_user_by_username(username):
        return jsonify({"error": "User already exists"}), 400

    user_model.create_user(username, role, password, public_key)
    return jsonify({"message": "User registered successfully"}), 201

def login():
    data = request.json
    username = data['username']
    password = data['password']
    user = user_model.find_user_by_username(username)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        token = jwt.encode({'user_id': str(user['_id']), 'role': user['role'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY)
        return jsonify({'token': token})

    return jsonify({"error": "Invalid credentials"}), 401
