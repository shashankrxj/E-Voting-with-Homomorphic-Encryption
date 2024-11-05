from flask import Blueprint
from controllers.voter_controller import cast_vote

voter_routes = Blueprint('voter_routes', __name__)

voter_routes.route('/cast', methods=['POST'])(cast_vote)
