"""
Flask application entry point for the restaurant recommendation system.

Initializes the app, database, and registers all API blueprints.

Usage:
    python app.py
"""
from flask import Flask
from flask_cors import CORS
from database.connection import db_connection
from api.user_routes import user_bp
from api.restaurant_routes import restaurant_bp
from recommendations import recommendations_bp, init_recommendations

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask app instance.
    """
    app = Flask(__name__)
    CORS(app)

    # Initialize database
    db = db_connection.get_db()

    # Initialize recommendations blueprint
    init_recommendations(db)

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(recommendations_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)