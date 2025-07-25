from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name')
})

@api.route('/')
class AmenityList(Resource):
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200
    
    @jwt_required()
    @api.expect(amenity_model)
    def post(self):
        """Create a new amenity (Admin only)"""
        current_user = get_jwt_identity()
        
        if not current_user['is_admin']:
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        
        try:
            amenity = facade.create_amenity(amenity_data)
            return amenity.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
    
    @jwt_required()
    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update amenity (Admin only)"""
        current_user = get_jwt_identity()
        
        if not current_user['is_admin']:
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        amenity = facade.update_amenity(amenity_id, amenity_data)
        
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        return amenity.to_dict(), 200
    
    @jwt_required()
    def delete(self, amenity_id):
        """Delete amenity (Admin only)"""
        current_user = get_jwt_identity()
        
        if not current_user['is_admin']:
            return {'error': 'Admin privileges required'}, 403
        
        if facade.delete_amenity(amenity_id):
            return {'message': 'Amenity deleted successfully'}, 200
        return {'error': 'Amenity not found'}, 404
