from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(description='Admin status')
})

@api.route('/')
class UserList(Resource):
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
    
    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Update user"""
        current_user = get_jwt_identity()
        
        # Only admin or owner can update
        if not current_user['is_admin'] and current_user['user_id'] != user_id:
            return {'error': 'Unauthorized'}, 403
        
        user_data = api.payload
        user = facade.update_user(user_id, user_data)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return user.to_dict(), 200
