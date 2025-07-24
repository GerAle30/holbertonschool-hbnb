from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services.facade import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """User login"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])
        
        if user and user.verify_password(credentials['password']):
            access_token = create_access_token(
                identity={'user_id': user.id, 'is_admin': user.is_admin}
            )
            return {'access_token': access_token}, 200
        
        return {'error': 'Invalid credentials'}, 401

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    def post(self):
        """User registration"""
        user_data = api.payload
        
        # Check if user already exists
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400
        
        try:
            user = facade.create_user(user_data)
            return {'message': 'User registered successfully', 'user_id': user.id}, 201
        except Exception as e:
            return {'error': str(e)}, 400
