from flask import request, jsonify
from models.user_model import User
from models.vote_model import Vote
from bson.objectid import ObjectId
from db import get_db
from phe import paillier

db = get_db()
user_model = User(db)
vote_model = Vote(db)

# Paillier keys (Assumed to be available)
public_key, private_key = paillier.generate_paillier_keypair()

def register_candidate():
    data = request.json
    username = data['username']
    password = data['password']
    role = 'candidate'

    if user_model.find_user_by_username(username):
        return jsonify({"error": "Candidate already exists"}), 400

    user_model.create_user(username, role, password)
    return jsonify({"message": "Candidate registered successfully"}), 201

def get_candidate_result(candidate_id):
    candidate = user_model.find_user_by_id(candidate_id)
    if not candidate or candidate['role'] != 'candidate':
        return jsonify({"error": "Candidate not found"}), 404

    # Fetch all votes for the candidate
    encrypted_votes = vote_model.collection.find({'candidate_id': ObjectId(candidate_id)})

    # Sum up the encrypted votes
    encrypted_sum = public_key.encrypt(0)
    for vote in encrypted_votes:
        encrypted_vote = paillier.EncryptedNumber(public_key, int(vote['encrypted_vote']))
        encrypted_sum += encrypted_vote

    # Decrypt to get the vote count
    decrypted_result = private_key.decrypt(encrypted_sum)
    
    return jsonify({"result": decrypted_result})
