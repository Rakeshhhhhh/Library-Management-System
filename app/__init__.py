from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()  # Declare db here first

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    
    # Register blueprints
    from .routes.main_routes import main_routes
    from .routes.book_routes import book_routes
    from .routes.member_routes import member_routes
    from .routes.transaction_routes import transaction_routes
    from .routes.report_routes import report_routes
    from .routes.search_routes import search_routes
    
    # Register blueprints with the app
    app.register_blueprint(main_routes) 
    app.register_blueprint(book_routes)
    app.register_blueprint(member_routes)
    app.register_blueprint(transaction_routes)
    app.register_blueprint(report_routes)
    app.register_blueprint(search_routes)

    # Import routes here after initializing db
    with app.app_context():
        db.create_all()
        
    return app