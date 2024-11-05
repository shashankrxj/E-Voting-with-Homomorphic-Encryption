from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import admin_collection, candidate_collection, voter_collection, reset_voting
from phe import paillier
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Generate Paillier keys (public and private keys for encryption)
public_key, private_key = paillier.generate_paillier_keypair()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Securely load secret key

# Route for the main interface
@app.route('/')
def index():
    return render_template('index.html')

# Route for the Administrator page
@app.route('/admin')
def admin_page():
    return render_template('admin.html')

# Route for the Candidate page
@app.route('/candidate')
def candidate_page():
    return render_template('candidate.html')

# Route for the Voter page
@app.route('/voter')
def voter_page():
    return render_template('voter.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    admin_user_id = session.get('user_id')

    if not admin_user_id:
        flash("You must be logged in as an admin to view the dashboard", "danger")
        return redirect(url_for('login'))

    # Retrieve the results stored in the logged-in admin's document
    admin_data = admin_collection.find_one({'user_id': admin_user_id})
    results = admin_data.get('results', {})  # Default to empty if no results found

    return render_template('admin_dashboard.html', results=results)


# Calculate Total Votes Route - Admin declares the result
@app.route('/calculate_totals', methods=['POST'])
def calculate_totals():
    # Get current admin's user_id from the session
    admin_user_id = session.get('user_id')

    if not admin_user_id:
        flash("You must be logged in as an admin to calculate totals", "danger")
        return redirect(url_for('admin_dashboard'))

    # Process vote totals
    candidates = candidate_collection.find()
    results = {}

    for candidate in candidates:
        encrypted_votes_str = candidate.get('encrypted_votes', '0')
        if encrypted_votes_str == '0':
            encrypted_vote = public_key.encrypt(0)
        else:
            encrypted_vote = paillier.EncryptedNumber(public_key, int(encrypted_votes_str), 0)

        decrypted_total_votes = private_key.decrypt(encrypted_vote)
        results[candidate['user_id']] = decrypted_total_votes

        candidate_collection.update_one(
            {'user_id': candidate['user_id']},
            {'$set': {'decrypted_votes': decrypted_total_votes}}
        )

    # Store the results in the admin record associated with the logged-in admin
    admin_collection.update_one(
        {'user_id': admin_user_id},
        {'$set': {'results': results}},
        upsert=True
    )

    return render_template('admin_dashboard.html', results=results)


# Route for Voter Dashboard
@app.route('/voter_dashboard')
def voter_dashboard():
    candidates = candidate_collection.find()  # Retrieve all candidates
    return render_template('voter_dashboard.html', candidates=candidates)

# Route to cast a vote - Encrypt and store the vote count
@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    if 'user_id' not in session:
        flash("You must be logged in to vote", "danger")
        return redirect(url_for('voter_dashboard'))

    voter_id = session['user_id']

    # Check if the voter has already voted
    voter = voter_collection.find_one({'user_id': voter_id})
    if voter.get('has_voted'):
        flash("You have already voted!", "danger")
        return redirect(url_for('voter_dashboard'))

    candidate_id = request.form.get('candidate_id')

    # Fetch the candidate data
    candidate = candidate_collection.find_one({'user_id': candidate_id})
    if not candidate:
        flash("Candidate not found", "danger")
        return redirect(url_for('voter_dashboard'))

    # Encrypt the vote (value = 1)
    encrypted_vote = public_key.encrypt(1)  # This encrypts the value of the vote.

    # Initialize current encrypted votes as a string from the database
    current_encrypted_votes_str = candidate.get('encrypted_votes', '0')  # String retrieved from MongoDB

    # Deserialize current encrypted votes from the string
    if current_encrypted_votes_str == '0':  # No previous votes
        current_encrypted_votes = public_key.encrypt(0)
    else:
        # Convert string back to integer for EncryptedNumber
        current_encrypted_votes = paillier.EncryptedNumber(
            public_key, int(current_encrypted_votes_str), 0  # <--- Key change: convert string to int
        )

    # Add the new encrypted vote to the current encrypted votes
    updated_encrypted_votes = current_encrypted_votes + encrypted_vote

    # Store the updated encrypted votes in the candidate database as a string
    candidate_collection.update_one(
        {'user_id': candidate_id},
        {'$set': {'encrypted_votes': str(updated_encrypted_votes.ciphertext())}}  # Store as string
    )

    # Mark voter as having voted
    voter_collection.update_one(
        {'user_id': voter_id},
        {'$set': {'has_voted': True}}  # This field is set to true after the voter has voted
    )

    flash(f"You have successfully cast your vote for candidate {candidate_id}!", "success")
    return redirect(url_for('voter_dashboard'))


# Route for Candidate Dashboard - Candidates should not see votes unless admin declared result
@app.route('/candidate_dashboard')
def candidate_dashboard():
    user_id = session.get('user_id')  # Get user_id from session
    candidate = candidate_collection.find_one({'user_id': user_id})

    if candidate is None:
        flash("Candidate not found!", "danger")
        return redirect(url_for('index'))  # Redirect to home if candidate not found

    decrypted_votes = candidate.get('decrypted_votes', 'Results not yet declared')

    return render_template('candidate_dashboard.html', votes=decrypted_votes)  # Show decrypted votes or message


# Common function for login and registration
@app.route('/login_register', methods=['POST'])
def login_register():
    role = request.form['role']  # Role: admin, candidate, voter
    user_id = request.form['user_id']
    password = request.form['password']
    action = request.form['action']  # Either 'login' or 'register'

    # Choose collection based on the role
    if role == 'admin':
        collection = admin_collection
        role_name = 'Administrator'
        register_redirect = 'admin_page'  # Redirect back to admin page after registration
        dashboard_redirect = 'admin_dashboard'  # Redirect to admin dashboard after login
    elif role == 'candidate':
        collection = candidate_collection
        role_name = 'Candidate'
        register_redirect = 'candidate_page'  # Redirect back to candidate page after registration
        dashboard_redirect = 'candidate_dashboard'  # Redirect to candidate dashboard after login
    elif role == 'voter':
        collection = voter_collection
        role_name = 'Voter'
        register_redirect = 'voter_page'  # Redirect back to voter page after registration
        dashboard_redirect = 'voter_dashboard'  # Redirect to voter dashboard after login
    else:
        flash("Invalid role specified", "danger")
        return redirect(url_for('index'))

    if action == 'login':
        user = collection.find_one({'user_id': user_id})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user_id  # Store user ID in session
            flash(f"{role_name} logged in successfully!", "success")
            return redirect(url_for(dashboard_redirect))  # Redirect to dashboard on successful login
        else:
            flash("Invalid ID or password", "danger")
            return redirect(url_for(register_redirect))  # Redirect back to the current page

    elif action == 'register':
        # Check if the user already exists
        existing_user = collection.find_one({'user_id': user_id})
        if existing_user:
            flash(f"{role_name} already exists with this ID!", "danger")
            return redirect(url_for(register_redirect))  # Redirect back to the current page

        # Hash the password and store it in the respective collection
        hashed_password = generate_password_hash(password)
        if role == 'voter':
            # For voters, we initialize has_voted to False
            collection.insert_one({'user_id': user_id, 'password': hashed_password, 'has_voted': False})
        else:
            collection.insert_one({'user_id': user_id, 'password': hashed_password})
        flash(f"{role_name} registered successfully!", "success")
        return redirect(url_for(register_redirect))  # Redirect back to the current page after registration


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    user_type = request.form.get('user_type')
    print(f'User type: {user_type}')  # Debug line to check user type

    if user_type == 'candidate':
        return redirect(url_for('candidate_page'))
    elif user_type == 'voter':
        return redirect(url_for('voter_page'))
    elif user_type == 'admin':
        return redirect(url_for('admin_page'))
    else:
        return redirect(url_for('index'))


# Route to reset the voting system
@app.route('/reset', methods=['POST'])
def reset_voting():
    # Remove all data from the collections
    admin_collection.delete_many({})       # Deletes all documents from the Admin collection
    voter_collection.delete_many({})       # Deletes all documents from the Voter collection
    candidate_collection.delete_many({})   # Deletes all documents from the Candidate collection
    
    # Optionally, reset any vote count or status as needed
    flash("Voting system reset! All data has been deleted.", "info")
    
    # Redirect to the main page after reset
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
