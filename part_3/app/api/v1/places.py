from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude')
})

@api.route('/')
class PlaceList(Resource):
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200
    
    @jwt_required()
    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user['user_id']
        
        try:
            place = facade.create_place(place_data)
            return place.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200
    
    @jwt_required()
    @api.expect(place_model)
    def put(self, place_id):
        """Update place"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Only owner or admin can update
        if not current_user['is_admin'] and place.owner_id != current_user['user_id']:
            return {'error': 'Unauthorized'}, 403
        
        place_data = api.payload
        updated_place = facade.update_place(place_id, place_data)
        return updated_place.to_dict(), 200
    
    @jwt_required()
    def delete(self, place_id):
        """Delete place"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Only owner or admin can delete
        if not current_user['is_admin'] and place.owner_id != current_user['user_id']:
            return {'error': 'Unauthorized'}, 403
        
        if facade.delete_place(place_id):
            return {'message': 'Place deleted successfully'}, 200
        return {'error': 'Failed to delete place'}, 400
