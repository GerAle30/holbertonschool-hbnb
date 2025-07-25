from flask import Blueprint
from flask_restx import Api

from .users import api as users_ns
from .places import api as places_ns
from .amenities import api as amenities_ns
from .reviews import api as reviews_ns
from .auth import api as auth_ns

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='HBnB API', description='Simplified HBnB API')

# Register namespaces
api.add_namespace(users_ns, path='/users')
api.add_namespace(places_ns, path='/places')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(reviews_ns, path='/reviews')
api.add_namespace(auth_ns, path='/auth')
