from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.utils.rbac import admin_required, get_current_user_info

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data or duplicate amenity name')
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only) - Enhanced admin verification"""
        # Enhanced admin privilege check using both get_jwt_identity() and get_jwt()
        current_user = get_jwt_identity()
        jwt_claims = get_jwt()
        
        # Check admin privileges from both identity and JWT claims
        is_admin = current_user.get('is_admin', False) or jwt_claims.get('is_admin', False)
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        # Get amenity data from request
        data = request.json
        if not data:
            return {'error': 'No data provided'}, 400
        
        # Enhanced validation
        name = data.get('name')
        if not name:
            return {'error': 'Missing required field: name'}, 400

        # Validate name is not empty or whitespace only
        if not name.strip():
            return {'error': 'Amenity name cannot be empty or whitespace'}, 400
        
        # Clean and standardize the name
        cleaned_name = name.strip()
            
        # Check for duplicate amenity names (case-insensitive)
        existing_amenities = facade.get_all_amenities()
        for amenity in existing_amenities:
            if amenity.name.lower() == cleaned_name.lower():
                return {'error': f'Amenity with name "{cleaned_name}" already exists'}, 400
        
        # Logic to create a new amenity
        try:
            amenity_data = {'name': cleaned_name}
            new_amenity = facade.create_amenity(amenity_data)
            
            if not new_amenity:
                return {'error': 'Failed to create amenity'}, 400
            
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat(),
                'message': 'Amenity successfully created by administrator',
                'created_by_admin': True
            }, 201
            
        except ValueError as ve:
            return {'error': f'Invalid amenity data: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Failed to create amenity: {str(e)}'}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            amenities = facade.get_all_amenities()
            return [
                {
                    'id': amenity.id,
                    'name': amenity.name,
                    'created_at': amenity.created_at.isoformat(),
                    'updated_at': amenity.updated_at.isoformat()
                }
                for amenity in amenities
            ], 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404

            return {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat(),
                'updated_at': amenity.updated_at.isoformat()
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data or duplicate name')
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (Admin only) - Enhanced admin verification"""
        # Enhanced admin privilege check using both get_jwt_identity() and get_jwt()
        current_user = get_jwt_identity()
        jwt_claims = get_jwt()
        
        # Check admin privileges from both identity and JWT claims
        is_admin = current_user.get('is_admin', False) or jwt_claims.get('is_admin', False)
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        # Get amenity data from request
        data = request.json
        if not data:
            return {'error': 'No data provided'}, 400
        
        # Enhanced validation
        name = data.get('name')
        if not name:
            return {'error': 'Missing required field: name'}, 400

        # Validate name is not empty or whitespace only
        if not name.strip():
            return {'error': 'Amenity name cannot be empty or whitespace'}, 400
        
        # Clean and standardize the name
        cleaned_name = name.strip()

        try:
            # Check if the amenity exists
            existing_amenity = facade.get_amenity(amenity_id)
            if not existing_amenity:
                return {'error': 'Amenity not found'}, 404

            # Check for duplicate names (excluding current amenity) - case-insensitive
            existing_amenities = facade.get_all_amenities()
            for amenity in existing_amenities:
                if (amenity.id != amenity_id and 
                    amenity.name.lower() == cleaned_name.lower()):
                    return {'error': f'Another amenity with name "{cleaned_name}" already exists'}, 400

            # Logic to update an amenity
            amenity_data = {'name': cleaned_name}
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            
            if not updated_amenity:
                return {'error': 'Failed to update amenity'}, 400
            
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat(),
                'updated_at': updated_amenity.updated_at.isoformat(),
                'message': 'Amenity successfully modified by administrator',
                'modified_by_admin': True
            }, 200

        except ValueError as ve:
            return {'error': f'Invalid amenity data: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}, 500
