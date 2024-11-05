from flask import Blueprint
from controllers.admin_controller import tally_votes

admin_routes = Blueprint('admin_routes', __name__)

admin_routes.route('/tally', methods=['GET'])(tally_votes)
