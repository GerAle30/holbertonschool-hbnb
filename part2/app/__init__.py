from flask import Flask
from flask_restx import Api


def create_app():
    app = Flask(__name__)

    # Register API blueprint
    from app.api.v1 import blueprint as api_v1
    app.register_blueprint(api_v1)

    return app
