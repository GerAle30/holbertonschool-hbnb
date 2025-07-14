"""
Complete JWT Authentication Implementation Example

This file demonstrates how JWT authentication is implemented across all protected endpoints
using the @jwt_required() decorator and get_jwt_identity() function.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

# Example 1: Places API with JWT Authentication
api = Namespace('places', description='Place operations')

# Define models
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Cannot create place for another user')
    @jwt_required()
    def post(self):
        """Create a new place - JWT Protected"""
        place_data = api.payload
        current_user = get_jwt_identity()
        
        # Step 1: Get current user information from JWT token
        user_id = current_user['id']
        is_admin = current_user.get('is_admin', False)
        
        # Step 2: Authorization check - Users can only create places for themselves
        if place_data.get('owner_id') != user_id and not is_admin:
            return {'error': 'Unauthorized to create place for another user'}, 403
        
        # Step 3: Validate input data
        if not place_data.get('title') or not place_data.get('title').strip():
            return {'error': 'Title cannot be empty'}, 400
        
        # Step 4: Create the place
        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.name,
                'owner_id': new_place.owner.id,
                'message': 'Place created successfully'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
    
    def get(self):
        """Retrieve all places - Public (no JWT required)"""
        places = facade.get_all_places()
        return [{'id': place.id, 'title': place.name} for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    def get(self, place_id):
        """Get place details - Public (no JWT required)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id, 'title': place.name}, 200
    
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Forbidden - Can only update own places')
    @jwt_required()
    def put(self, place_id):
        """Update a place - JWT Protected"""
        place_data = api.payload
        current_user = get_jwt_identity()
        
        # Step 1: Get current user information
        user_id = current_user['id']
        is_admin = current_user.get('is_admin', False)
        
        # Step 2: Check if place exists
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404
        
        # Step 3: Authorization check - Users can only update their own places
        if existing_place.owner.id != user_id and not is_admin:
            return {'error': 'Unauthorized to update this place'}, 403
        
        # Step 4: Update the place
        try:
            updated_place = facade.update_place(place_id, place_data)
            return {
                'id': updated_place.id,
                'title': updated_place.name,
                'message': 'Place updated successfully'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


# Example 2: Reviews API with JWT Authentication
reviews_api = Namespace('reviews', description='Review operations')

review_model = reviews_api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

@reviews_api.route('/')
class ReviewList(Resource):
    @reviews_api.expect(review_model)
    @reviews_api.response(201, 'Review created successfully')
    @reviews_api.response(403, 'Forbidden - Cannot review own place')
    @jwt_required()
    def post(self):
        """Create a new review - JWT Protected"""
        review_data = api.payload
        current_user = get_jwt_identity()
        
        # Step 1: Get current user information
        user_id = current_user['id']
        
        # Step 2: Validate user can only create reviews for themselves
        if review_data.get('user_id') != user_id:
            return {'error': 'Cannot create review for another user'}, 403
        
        # Step 3: Check if place exists
        place = facade.get_place(review_data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Step 4: Business logic - Users cannot review their own places
        if place.owner.id == user_id:
            return {'error': 'Cannot review your own place'}, 403
        
        # Step 5: Check for duplicate reviews
        existing_reviews = facade.get_reviews_by_place(review_data.get('place_id'))
        for review in existing_reviews:
            if review.user.id == user_id:
                return {'error': 'You have already reviewed this place'}, 403
        
        # Step 6: Create the review
        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.comment,
                'rating': new_review.rating,
                'message': 'Review created successfully'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@reviews_api.route('/<review_id>')
class ReviewResource(Resource):
    @reviews_api.expect(review_model)
    @reviews_api.response(200, 'Review updated successfully')
    @reviews_api.response(403, 'Forbidden - Can only update own reviews')
    @jwt_required()
    def put(self, review_id):
        """Update a review - JWT Protected"""
        review_data = api.payload
        current_user = get_jwt_identity()
        
        # Step 1: Get current user information
        user_id = current_user['id']
        is_admin = current_user.get('is_admin', False)
        
        # Step 2: Check if review exists
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        
        # Step 3: Authorization check - Users can only update their own reviews
        if existing_review.user.id != user_id and not is_admin:
            return {'error': 'Can only update your own reviews'}, 403
        
        # Step 4: Prevent changing ownership
        if 'user_id' in review_data and review_data['user_id'] != existing_review.user.id:
            return {'error': 'Cannot change review ownership'}, 403
        
        # Step 5: Update the review
        try:
            updated_review = facade.update_review(review_id, review_data)
            return {
                'id': updated_review.id,
                'text': updated_review.comment,
                'rating': updated_review.rating,
                'message': 'Review updated successfully'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    @reviews_api.response(200, 'Review deleted successfully')
    @reviews_api.response(403, 'Forbidden - Can only delete own reviews')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review - JWT Protected"""
        current_user = get_jwt_identity()
        
        # Step 1: Get current user information
        user_id = current_user['id']
        is_admin = current_user.get('is_admin', False)
        
        # Step 2: Check if review exists
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        
        # Step 3: Authorization check - Users can only delete their own reviews
        if existing_review.user.id != user_id and not is_admin:
            return {'error': 'Can only delete your own reviews'}, 403
        
        # Step 4: Delete the review
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        
        return {'message': 'Review deleted successfully'}, 200


# Example 3: Users API with JWT Authentication
users_api = Namespace('users', description='User operations')

user_update_model = users_api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})

@users_api.route('/<user_id>')
class UserResource(Resource):
    @users_api.expect(user_update_model)
    @users_api.response(200, 'User updated successfully')
    @users_api.response(403, 'Forbidden - Can only update own profile')
    @jwt_required()
    def put(self, user_id):
        """Update user profile - JWT Protected"""
        user_data = api.payload
        current_user = get_jwt_identity()
        
        # Step 1: Get current user information
        current_user_id = current_user['id']
        is_admin = current_user.get('is_admin', False)
        
        # Step 2: Authorization check - Users can only update their own profile
        if current_user_id != user_id and not is_admin:
            return {'error': 'Unauthorized to update this user'}, 403
        
        # Step 3: Validate allowed fields
        allowed_fields = {'first_name', 'last_name'}
        invalid_fields = set(user_data.keys()) - allowed_fields
        if invalid_fields:
            return {'error': f'Cannot update fields: {list(invalid_fields)}'}, 400
        
        # Step 4: Update the user
        try:
            updated_user = facade.update_user(user_id, user_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'message': 'User updated successfully'
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


# JWT Authentication Pattern Summary:
"""
Common JWT Implementation Pattern:

1. Import required modules:
   from flask_jwt_extended import jwt_required, get_jwt_identity

2. Add @jwt_required() decorator to protected methods:
   @jwt_required()
   def post(self):
       # Protected method

3. Get current user information:
   current_user = get_jwt_identity()
   user_id = current_user['id']
   is_admin = current_user.get('is_admin', False)

4. Implement authorization logic:
   - Check resource ownership
   - Validate admin privileges
   - Enforce business rules

5. Handle errors appropriately:
   - 401: Unauthorized (invalid/missing token)
   - 403: Forbidden (valid token, insufficient permissions)
   - 404: Not found
   - 400: Bad request

Key Security Features:
- JWT token validation on every request
- User identity extraction from token
- Resource ownership verification
- Admin privilege escalation
- Business rule enforcement
- Comprehensive error handling
"""
