from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.utils.rbac import check_admin_or_owner, get_current_user_info

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True,
                             description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Define the review update model (all fields optional)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user (cannot be changed)'),
    'place_id': fields.String(description='ID of the place (cannot be changed)')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Bad Request - Cannot review own place or already reviewed')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()
        
        # Ensure the user_id in the payload matches the current user
        if review_data.get('user_id') != current_user['id']:
            return {'error': 'Cannot create review for another user'}, 403
        
        # Check if the place exists and get place details
        place = facade.get_place(review_data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404
            
        # Users cannot review their own places
        if place.owner.id == current_user['id']:
            return {'error': 'You cannot review your own place.'}, 400
            
        # Check if user has already reviewed this place
        existing_reviews = facade.get_reviews_by_place(review_data.get('place_id'))
        for review in existing_reviews:
            if review.user.id == current_user['id']:
                return {'error': 'You have already reviewed this place.'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            } for review in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Forbidden - Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information - Admin bypass ownership restrictions"""
        current_user = get_jwt_identity()
        jwt_claims = get_jwt()
        
        # Enhanced admin privilege check using both identity and claims
        is_admin = current_user.get('is_admin', False) or jwt_claims.get('is_admin', False)
        user_id = current_user.get('id')

        # Get the review data from request
        review_data = request.json
        if not review_data:
            return {'error': 'No data provided'}, 400

        # Get the existing review to check ownership
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        # Admin bypass ownership restrictions - exact implementation as specified
        if not is_admin and review.user.id != user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            # Logic to update the review - comprehensive validation
            
            # Prevent changing user_id and place_id in updates
            if 'user_id' in review_data and review_data['user_id'] != review.user.id:
                return {'error': 'Cannot change review ownership'}, 403
            if 'place_id' in review_data and review_data['place_id'] != review.place.id:
                return {'error': 'Cannot change review place'}, 403
            
            # Update the review using facade
            updated_review = facade.update_review(review_id, review_data)

            if not updated_review:
                return {'error': 'Failed to update review'}, 400

            # Prepare response with admin bypass tracking
            response_data = {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id,
                'place_id': updated_review.place.id,
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }

            # Add admin modification tracking if admin performed the update
            if is_admin and review.user.id != user_id:
                response_data['message'] = 'Review successfully modified by administrator'
                response_data['updated_by_admin'] = True
            else:
                response_data['message'] = 'Review successfully updated'

            return response_data, 200
        except ValueError as ve:
            return {'error': f'Invalid data: {str(ve)}'}, 400
        except Exception as e:
            return {'error': f'Update failed: {str(e)}'}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Forbidden - Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review - Admin bypass ownership restrictions"""
        current_user = get_jwt_identity()
        jwt_claims = get_jwt()
        
        # Enhanced admin privilege check using both identity and claims
        is_admin = current_user.get('is_admin', False) or jwt_claims.get('is_admin', False)
        user_id = current_user.get('id')
        
        # Get the existing review to check ownership
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
            
        # Admin bypass ownership restrictions - exact implementation as specified
        if not is_admin and review.user.id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            # Delete the review using facade
            success = facade.delete_review(review_id)
            if not success:
                return {'error': 'Failed to delete review'}, 400
            
            # Prepare response with admin bypass tracking
            response_data = {'message': 'Review deleted successfully'}
            
            # Add admin deletion tracking if admin performed the deletion
            if is_admin and review.user.id != user_id:
                response_data['deleted_by_admin'] = True
                response_data['message'] = 'Review deleted by administrator'
            
            return response_data, 200
            
        except Exception as e:
            return {'error': f'Delete failed: {str(e)}'}, 500


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'id': review.id,
                    'text': review.comment,
                    'rating': review.rating,
                    'user_id': review.user.id,
                    'place_id': review.place.id,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat()
                } for review in reviews
            ], 200
        except ValueError as e:
            return {'error': str(e)}, 404
