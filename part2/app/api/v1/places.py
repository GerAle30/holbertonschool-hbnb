from flask_restx import Namespace, Resource, fields
from app.services import facade

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

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload

        try:
            # Validate required fields
            required_fields = ['title', 'price', 'latitude', 'longitude',
                               'owner_id']
            for field in required_fields:
                if field not in place_data or place_data[field] is None:
                    return {'error': f'Missing required field: {field}'}, 400

            # Validate data types and ranges
            if (not isinstance(place_data['price'], (int, float)) or
                    place_data['price'] <= 0):
                return {'error': 'Price must be a positive number'}, 400

            if (not isinstance(place_data['latitude'], (int, float)) or
                    not (-90 <= place_data['latitude'] <= 90)):
                return {'error': 'Latitude must be between -90 and 90'}, 400

            if (not isinstance(place_data['longitude'], (int, float)) or
                    not (-180 <= place_data['longitude'] <= 180)):
                return {'error':
                        'Longitude must be between -180 and 180'}, 400

            # Create the place using the facade
            new_place = facade.create_place(place_data)

            return {
                'id': new_place.id,
                'title': new_place.name,  # Map name to title
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner.id,
                'amenities': [amenity.id for amenity in new_place.amenities],
                'created_at': new_place.created_at.isoformat(),
                'updated_at': new_place.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        pass


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
            return {
                'id': place.id,
                'title': place.name,  # Map name back to title
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
                'amenities': [{
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in place.amenities],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload

        try:
            # Check the place exists
            existing_place = facade.get_place(place_id)
            if not existing_place:
                return {'error': 'Place not found'}, 404

            # Validate data types and ranges
            if 'price' in place_data:
                if (not isinstance(place_data['price'], (int, float)) or
                        place_data['price'] <= 0):
                    return {'error':
                            'Price must be a positive number'}, 400

            if 'latitude' in place_data:
                if (not isinstance(place_data['latitude'], (int, float)) or
                        not (-90 <= place_data['latitude'] <= 90)):
                    return {'error':
                            'Latitude must be between -90 and 90'}, 400

            if 'longitude' in place_data:
                if (not isinstance(place_data['longitude'], (int, float)) or
                        not (-180 <= place_data['longitude'] <= 180)):
                    return {'error':
                            'Longitude must be between -180 and 180'}, 400

            # Update the place using facade
            updated_place = facade.update_place(place_id, place_data)

            if not updated_place:
                return {'error': 'Place not found'}, 404
            return {
                'id': updated_place.id,
                'title': updated_place.name,  # Map name back to title
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'owner': {
                    'id': updated_place.owner.id,
                    'first_name': updated_place.owner.first_name,
                    'last_name': updated_place.owner.last_name,
                    'email': updated_place.owner.email
                },
                'amenities': [{
                    'id': amenity.id,
                    'name': amenity.name
                } for amenity in updated_place.amenities],
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 500


# Adding the model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model),
                             description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model),
                           description='List of reviews')
})
