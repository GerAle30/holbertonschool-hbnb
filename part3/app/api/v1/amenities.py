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
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    @admin_required
    def post(self):
        """Register a new amenity (Admin only)"""
        amenity_data = api.payload
        
        # Enhanced validation
        if not amenity_data or 'name' not in amenity_data:
            return {'error': 'Missing required field: name'}, 400

        name = amenity_data['name']
        if not name or not name.strip():
            return {'error': 'Name cannot be empty'}, 400
            
        # Check for duplicate amenity names
        existing_amenities = facade.get_all_amenities()
        for amenity in existing_amenities:
            if amenity.name.lower() == name.strip().lower():
                return {'error': 'Amenity with this name already exists'}, 400
        
        try:
            # Create the amenity using the facade
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat(),
                'message': 'Amenity successfully created'
            }, 201
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

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    @admin_required
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        amenity_data = api.payload
        
        # Enhanced validation
        if not amenity_data or 'name' not in amenity_data:
            return {'error': 'Missing required field: name'}, 400

        name = amenity_data['name']
        if not name or not name.strip():
            return {'error': 'Name cannot be empty'}, 400

        try:
            # Check if the amenity exists
            existing_amenity = facade.get_amenity(amenity_id)
            if not existing_amenity:
                return {'error': 'Amenity not found'}, 404

            # Check for duplicate names (excluding current amenity)
            existing_amenities = facade.get_all_amenities()
            for amenity in existing_amenities:
                if (amenity.id != amenity_id and 
                    amenity.name.lower() == name.strip().lower()):
                    return {'error': 'Another amenity with this name already exists'}, 400

            # Update the amenity using the facade
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if updated_amenity:
                return {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name,
                    'created_at': updated_amenity.created_at.isoformat(),
                    'updated_at': updated_amenity.updated_at.isoformat(),
                    'message': 'Amenity successfully updated'
                }, 200
            else:
                return {'error': 'Failed to update amenity'}, 400

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}, 500
