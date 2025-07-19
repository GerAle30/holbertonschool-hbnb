from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize Bcrypt
    bcrypt.init_app(app)
    
    # Initialize JWT
    jwt.init_app(app)

    # Import models to ensure they are registered with SQLAlchemy
    from app.models.user import User
    
    # Register API blueprint
    from app.api.v1 import blueprint as api_v1
    app.register_blueprint(api_v1)

    return app
