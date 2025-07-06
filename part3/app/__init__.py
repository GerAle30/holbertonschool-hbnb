from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize Bcrypt
    bcrypt.init_app(app)
    
    # Initialize JWT
    jwt.init_app(app)

    # Register API blueprint
    from app.api.v1 import blueprint as api_v1
    app.register_blueprint(api_v1)

    return app
