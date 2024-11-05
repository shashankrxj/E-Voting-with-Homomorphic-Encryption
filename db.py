from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve MONGO_URI from the environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Establish MongoDB connection
client = MongoClient(MONGO_URI)


# Database name (e.g., 'Voting')
db = client['Voting']

# Admin collection schema: storing admin user_id and hashed password
admin_collection = db['Admin']
admin_collection.create_index('user_id', unique=True)  # Ensure unique user_id

# Candidate collection schema: storing candidate user_id, hashed password, and votes
candidate_collection = db['Candidate']
candidate_collection.create_index('user_id', unique=True)  # Ensure unique user_id

# Voter collection schema: storing voter user_id, hashed password, and voting status
voter_collection = db['Voter']
voter_collection.create_index('user_id', unique=True)  # Ensure unique user_id

# Example schema structure for each collection

# Admin collection: stores the user ID and password for the admin
# {
#   'user_id': 'admin1',
#   'password': 'hashed_password_string',
# }

# Candidate collection: stores the user ID, password, and vote count for candidates
# {
#   'user_id': 'candidate1',
#   'password': 'hashed_password_string',
#   'votes': 0  # This field will store the total votes received by the candidate
# }

# Voter collection: stores the user ID, password, and whether the voter has already voted
# {
#   'user_id': 'voter1',
#   'password': 'hashed_password_string',
#   'has_voted': False  # This field will indicate if the voter has already cast their vote
# }

# Reset functionality to clear votes and reset voters' voting status
def reset_voting():
    # Reset vote counts for candidates
    candidate_collection.update_many({}, {'$set': {'votes': 0}})
    # Reset voting status for all voters
    voter_collection.update_many({}, {'$set': {'has_voted': False}})

# Make sure to add a method to initialize the database if required
def initialize_db():
    # Ensure candidates have a votes field initialized
    for candidate in candidate_collection.find():
        if 'votes' not in candidate:
            candidate_collection.update_one({'_id': candidate['_id']}, {'$set': {'votes': 0}})
