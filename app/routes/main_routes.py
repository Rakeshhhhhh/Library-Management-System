from flask import Blueprint, render_template

# Create Blueprint
main_routes = Blueprint('main_routes', __name__)

# Default Home Route
@main_routes.route('/')
def index():
    return render_template('home.html')
