from flask import jsonify
from models.vote_model import Vote
from phe import paillier
from db import get_db 

db = get_db()
vote_model = Vote(db)

# Paillier keys (in practice, should be securely stored)
public_key, private_key = paillier.generate_paillier_keypair()

def tally_votes():
    votes = vote_model.get_votes()
    encrypted_sum = public_key.encrypt(0)  # Initialize encrypted sum

    for vote in votes:
        encrypted_vote = paillier.EncryptedNumber(public_key, int(vote['encrypted_vote']))
        encrypted_sum += encrypted_vote

    decrypted_result = private_key.decrypt(encrypted_sum)
    return jsonify({"result": decrypted_result})

def reset_votes():
    vote_model.delete_votes()
    user_model.collection.update_many({'role': 'voter'}, {'$set': {'has_voted': False}})
    return jsonify({"message": "Votes reset successfully"}), 200

