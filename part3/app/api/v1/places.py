from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.utils.rbac import check_admin_or_owner, get_current_user_info

api = Namespace('places', description='Place operations')

# Define models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    # owner_id is automatically set from JWT token, not required in input
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model),
                             description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model),
                           description='List of reviews')
})

# Define place update model (all fields optional)
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String,
                             description="List of amenities ID's")
})


def serialize_place(place):
    """Serialize a place object to a dictionary for JSON response."""
    # Get reviews for this place
    try:
        reviews = facade.get_reviews_by_place(place.id)
        reviews_data = [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id
            }
            for review in reviews
        ]
    except Exception:
        reviews_data = []

    return {
        'id': place.id,
        'title': place.title,  # Using correct attribute name
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner': {
            'id': place.owner.id,
            'first_name': place.owner.first_name,
            'last_name': place.owner.last_name,
            'email': place.owner.email
        },
        'amenities': [
            {
                'id': amenity.id if hasattr(amenity, 'id')
                else str(amenity),
                'name': amenity.name if hasattr(amenity, 'name')
                else 'Unknown Amenity'
            }
            for amenity in place.amenities
        ],
        'reviews': reviews_data,
        'created_at': place.created_at.isoformat(),
        'updated_at': place.updated_at.isoformat()
    }


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload
        # Get comprehensive user info using RBAC utilities
        user_info = get_current_user_info()
        current_user_id = user_info['user_id']
        is_admin = user_info['is_admin']
        
        # Ensure the user is authenticated
        if not current_user_id:
            return {'error': 'Authentication required'}, 401
        
        # Automatically set owner_id to the authenticated user's ID
        # This ensures users can only create places for themselves
        place_data['owner_id'] = current_user_id
        
        # Validate required fields (owner_id is now automatically set)
        required_fields = ['title', 'price', 'latitude', 'longitude']
        for field in required_fields:
            if not place_data or field not in place_data:
                error_msg = f'Missing required field: {field}'
                return {'error': error_msg}, 400

        # Validate title is not empty
        if not place_data['title'] or not place_data['title'].strip():
            return {'error': 'Title cannot be empty'}, 400

        # Validate price is positive
        try:
            price = float(place_data['price'])
            if price <= 0:
                return {'error': 'Price must be a positive number'}, 400
        except (ValueError, TypeError):
            return {'error': 'Price must be a valid number'}, 400

        # Validate latitude range (-90 to 90)
        try:
            latitude = float(place_data['latitude'])
            if latitude < -90 or latitude > 90:
                return {'error': 'Latitude must be between -90 and 90'}, 400
        except (ValueError, TypeError):
            return {'error': 'Latitude must be a valid number'}, 400

        # Validate longitude range (-180 to 180)
        try:
            longitude = float(place_data['longitude'])
            if longitude < -180 or longitude > 180:
                return {'error': 'Longitude must be between -180 and 180'}, 400
        except (ValueError, TypeError):
            return {'error': 'Longitude must be a valid number'}, 400

        # Ensure amenities is a list (optional field)
        if 'amenities' not in place_data:
            place_data['amenities'] = []
        elif not isinstance(place_data['amenities'], list):
            return {'error': 'Amenities must be a list'}, 400

        try:
            # Create the place using the facade
            new_place = facade.create_place(place_data)
            return serialize_place(new_place), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return [serialize_place(place) for place in places], 200
        except Exception as e:
            return {'error': str(e)}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            return serialize_place(place), 200
        except Exception as e:
            return {'error': str(e)}, 500

    @api.expect(place_update_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information - Admin bypass ownership restrictions"""
        current_user = get_jwt_identity()
        jwt_claims = get_jwt()
        
        # Enhanced admin privilege check using both identity and claims
        is_admin = current_user.get('is_admin', False) or jwt_claims.get('is_admin', False)
        user_id = current_user.get('id')
        
        # Validate that we have some data to update
        place_data = request.json
        if not place_data:
            return {'error': 'No data provided for update'}, 400

        try:
            # Check the place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
                
            # Admin bypass ownership restrictions - exact implementation as specified
            if not is_admin and place.owner.id != user_id:
                return {'error': 'Unauthorized action'}, 403

            # Logic to update the place - comprehensive validation
            
            # Validate title if provided
            if 'title' in place_data:
                if not place_data['title'] or not place_data['title'].strip():
                    return {'error': 'Title cannot be empty'}, 400

            # Validate price if provided
            if 'price' in place_data:
                try:
                    price = float(place_data['price'])
                    if price <= 0:
                        return {'error': 'Price must be a positive number'}, 400
                except (ValueError, TypeError):
                    return {'error': 'Price must be a valid number'}, 400

            # Validate latitude if provided
            if 'latitude' in place_data:
                try:
                    latitude = float(place_data['latitude'])
                    if latitude < -90 or latitude > 90:
                        return {'error': 'Latitude must be between -90 and 90'}, 400
                except (ValueError, TypeError):
                    return {'error': 'Latitude must be a valid number'}, 400

            # Validate longitude if provided
            if 'longitude' in place_data:
                try:
                    longitude = float(place_data['longitude'])
                    if longitude < -180 or longitude > 180:
                        return {'error': 'Longitude must be between -180 and 180'}, 400
                except (ValueError, TypeError):
                    return {'error': 'Longitude must be a valid number'}, 400

            # Validate amenities if provided
            if 'amenities' in place_data:
                if not isinstance(place_data['amenities'], list):
                    return {'error': 'Amenities must be a list'}, 400

            # Update the place using facade
            updated_place = facade.update_place(place_id, place_data)

            if not updated_place:
                return {'error': 'Failed to update place'}, 400

            # Prepare response with admin bypass tracking
            response_data = serialize_place(updated_place)
            
            # Add admin modification tracking if admin performed the update
            if is_admin and place.owner.id != user_id:
                response_data['message'] = 'Place successfully modified by administrator'
                response_data['modified_by_admin'] = True
            else:
                response_data['message'] = 'Place successfully updated'

            return response_data, 200

        except ValueError as ve:
            return {'error': f'Invalid data: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}, 500
    
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Forbidden - Unauthorized action')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place with enhanced RBAC"""
        # Get comprehensive user info using RBAC utilities
        user_info = get_current_user_info()
        current_user_id = user_info['user_id']
        is_admin = user_info['is_admin']
        
        try:
            # Check if the place exists
            existing_place = facade.get_place(place_id)
            if not existing_place:
                return {'error': 'Place not found'}, 404
            
            # Enhanced authorization check using RBAC
            is_authorized, current_user, admin_status = check_admin_or_owner(existing_place.owner.id)
            if not is_authorized:
                return {'error': 'Unauthorized action.'}, 403
            
            # Delete the place using facade
            success = facade.delete_place(place_id)
            if not success:
                return {'error': 'Failed to delete place'}, 400
            
            return {
                'message': 'Place deleted successfully',
                'deleted_by_admin': admin_status
            }, 200
            
        except Exception as e:
            return {'error': f'Delete failed: {str(e)}'}, 500
