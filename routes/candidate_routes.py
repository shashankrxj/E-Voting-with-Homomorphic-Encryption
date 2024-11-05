from flask import Blueprint
from controllers.candidate_controller import register_candidate, get_candidate_result

candidate_routes = Blueprint('candidate_routes', __name__)

# Register as a candidate
candidate_routes.route('/register', methods=['POST'])(register_candidate)

# View election result for a candidate
candidate_routes.route('/result/<candidate_id>', methods=['GET'])(get_candidate_result)
