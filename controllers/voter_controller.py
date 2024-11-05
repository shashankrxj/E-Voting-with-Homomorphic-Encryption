from flask import request, jsonify
from models.user_model import User
from models.vote_model import Vote
from phe import paillier
from db import get_db
from bson.objectid import ObjectId

db = get_db()
user_model = User(db)
vote_model = Vote(db)

# Paillier public key (Assumed to be available for encryption)
public_key, private_key = paillier.generate_paillier_keypair()

def cast_vote():
    data = request.json
    voter_id = data['voter_id']
    candidate_id = data['candidate_id']

    voter = user_model.find_user_by_id(voter_id)
    if voter['has_voted']:
        return jsonify({"error": "You have already voted"}), 403

    # Encrypt the vote
    encrypted_vote = public_key.encrypt(1)  # 1 represents the vote

    vote_model.cast_vote(candidate_id, encrypted_vote.ciphertext())
    user_model.update_user(voter_id, {'has_voted': True})

    return jsonify({"message": "Vote cast successfully"}), 201
