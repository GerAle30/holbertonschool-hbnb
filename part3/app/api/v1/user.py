from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Define the user response model (without password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Define the user update model (excluding email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})


@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [{'id': user.id, 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'email': user.email} for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real
        # validation for persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create user with password hashing handled by facade
        new_user = facade.create_user(user_data)
        
        return {'id': new_user.id, 'message': 'User successfully created'}, 201


@api.route('/<user_id>')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by id"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Can only update own profile')
    @jwt_required()
    def put(self, user_id):
        """Update a user's information (first_name and last_name only)"""
        user_data = api.payload
        current_user = get_jwt_identity()
        
        # Check the user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
            
        # Check if current user is authorized to update this user
        # Users can only update their own profile, admins can update any profile
        if current_user['id'] != user_id and not current_user.get('is_admin', False):
            return {'error': 'Unauthorized to update this user'}, 403

        # Validate that only allowed fields are being updated
        allowed_fields = {'first_name', 'last_name'}
        invalid_fields = set(user_data.keys()) - allowed_fields
        if invalid_fields:
            return {'error': f'Cannot update fields: {list(invalid_fields)}. Only first_name and last_name can be updated.'}, 400

        # Validate that we have some data to update
        if not user_data:
            return {'error': 'No valid data provided for update'}, 400

        # Update the user
        updated_user = facade.update_user(user_id, user_data)
        return {'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email}, 200
