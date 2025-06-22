from flask_restx import Api
from flask import Blueprint

from .user import api as user_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='HBnB API',
          description='API for HBnB app')

# Register namespaces
api.add_namespace(user_ns, path='/users')
