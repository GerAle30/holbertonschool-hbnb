from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Import models to register them with SQLAlchemy
    from app.models.user import User
    from app.models.place import Place
    from app.models.amenity import Amenity
    from app.models.review import Review
    
    # Register API blueprints
    from app.api.v1 import blueprint as api_v1
    app.register_blueprint(api_v1)
    
    return app
