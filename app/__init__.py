"""
Flask application initialization
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_class='config.Config'):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Fix PostgreSQL URL if needed (Render uses postgresql:// but SQLAlchemy needs postgresql+psycopg2://)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql+psycopg2://', 1)
    
    # Initialize extensions
    db.init_app(app)
    
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['KEYS_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app import routes
    app.register_blueprint(routes.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
