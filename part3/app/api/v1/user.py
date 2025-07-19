from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app.services import facade
from app.utils.rbac import admin_required, check_admin_or_owner, get_current_user_info

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status (only for admins)')
})

# Define the user response model (without password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Define the user update model (email and password restricted for regular users)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user (admin only)'),
    'password': fields.String(description='Password of the user (admin only)'),
    'is_admin': fields.Boolean(description='Admin status (admin only)')
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
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    @admin_required
    def post(self):
        """Register a new user (Admin only)"""
        user_data = api.payload
        
        # Enhanced email uniqueness check
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Create user with password hashing handled by facade
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id, 
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin,
                'message': 'User successfully created'
            }, 201
        except Exception as e:
            return {'error': f'Failed to create user: {str(e)}'}, 400


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
    @api.response(403, 'Forbidden - Unauthorized action')
    @api.response(400, 'Bad Request - Cannot modify email or password')
    @jwt_required()
    def put(self, user_id):
        """Modify user information - Administrators can modify any user including email and password"""
        user_data = api.payload
        
        # Get comprehensive user info using RBAC utilities
        user_info = get_current_user_info()
        current_user_id = user_info['user_id']
        is_admin = user_info['is_admin']
        
        # Check the user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
            
        # Enhanced authorization check using RBAC
        is_authorized, current_user, admin_status = check_admin_or_owner(user_id)
        if not is_authorized:
            return {'error': 'Unauthorized action.'}, 403

        # Email uniqueness validation - ensure email is not duplicated
        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # For regular users, restrict sensitive field modifications
        if not is_admin:
            restricted_fields = {'email', 'password', 'is_admin'}
            invalid_fields = set(user_data.keys()) & restricted_fields
            
            if invalid_fields:
                return {
                    'error': f'Regular users cannot modify: {list(invalid_fields)}. Admin privileges required.'
                }, 403

            # Validate that only allowed fields are being updated for regular users
            allowed_fields = {'first_name', 'last_name'}
            invalid_fields = set(user_data.keys()) - allowed_fields
            if invalid_fields:
                return {
                    'error': f'Invalid fields: {list(invalid_fields)}. Regular users can only update first_name and last_name.'
                }, 400
        
        # Validate that we have some data to update
        if not user_data:
            return {'error': 'No valid data provided for update'}, 400

        try:
            # Update the user - admins can modify any field including sensitive ones
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'Failed to update user'}, 400
            
            # Prepare response with admin modification tracking
            response_data = {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin
            }
            
            # Add appropriate message based on who performed the update
            if is_admin and current_user_id != user_id:
                response_data['message'] = 'User successfully modified by administrator'
                response_data['modified_by_admin'] = True
            else:
                response_data['message'] = 'User successfully updated'
                
            return response_data, 200
            
        except ValueError as ve:
            return {'error': f'Invalid data: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}, 400
