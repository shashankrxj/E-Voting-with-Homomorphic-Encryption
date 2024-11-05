from pymongo import MongoClient
from bson.objectid import ObjectId

class Vote:
    def __init__(self, db):
        self.collection = db['votes']

    def cast_vote(self, candidate_id, encrypted_vote):
        vote_data = {
            'candidate_id': ObjectId(candidate_id),
            'encrypted_vote': encrypted_vote
        }
        return self.collection.insert_one(vote_data)
    
    def get_votes(self):
        return list(self.collection.find({}))
    
    def delete_votes(self):
        return self.collection.delete_many({})
