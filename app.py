"""
Main Flask application entry point for the Online Shop Backend API.

This module initializes the Flask application, configures the database,
and sets up all the API routes for managing customers, categories, items, and orders.
"""

from flask import Flask
from models import db
from schema import create_all_tables, init_test_data
import os


def create_app():
    """Application factory pattern for creating Flask app"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Initialize database
    db.init_app(app)
    
    # Register routes
    from crud import register_routes
    register_routes(app)
    
    return app


def init_database(app):
    """Initialize database with tables and test data"""
    with app.app_context():
        print("Initializing database...")
        create_all_tables()
        
        # Check if database is empty and add test data
        from models import Customer
        if Customer.query.count() == 0:
            print("Database is empty, adding test data...")
            init_test_data()
            print("✅ Test data added successfully!")
        else:
            print("Database already contains data.")


if __name__ == '__main__':
    # Create the Flask application
    app = create_app()
    
    # Initialize database
    init_database(app)
    
    # Run the application
    print("🚀 Starting Online Shop Backend API...")
    print("📊 API Documentation:")
    print("   Customers: GET/POST /customers, GET/PUT/DELETE /customers/<id>")
    print("   Categories: GET/POST /categories, GET/PUT/DELETE /categories/<id>")
    print("   Items: GET/POST /items, GET/PUT/DELETE /items/<id>")
    print("   Orders: GET/POST /orders, GET/PUT/DELETE /orders/<id>")
    print("💡 Access the API at: http://localhost:5001")
    
    app.run(debug=True, host='0.0.0.0', port=5001)