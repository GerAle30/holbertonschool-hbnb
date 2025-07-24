from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200
    
    @jwt_required()
    @api.expect(review_model)
    def post(self):
        """Create a new review"""
        current_user = get_jwt_identity()
        review_data = api.payload
        review_data['user_id'] = current_user['user_id']
        
        # Validate rating
        if not (1 <= review_data['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        # Check if place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        try:
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200
    
    @jwt_required()
    @api.expect(review_model)
    def put(self, review_id):
        """Update review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Only owner or admin can update
        if not current_user['is_admin'] and review.user_id != current_user['user_id']:
            return {'error': 'Unauthorized'}, 403
        
        review_data = api.payload
        
        # Validate rating if provided
        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            return {'error': 'Rating must be between 1 and 5'}, 400
        
        updated_review = facade.update_review(review_id, review_data)
        return updated_review.to_dict(), 200
    
    @jwt_required()
    def delete(self, review_id):
        """Delete review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Only owner or admin can delete
        if not current_user['is_admin'] and review.user_id != current_user['user_id']:
            return {'error': 'Unauthorized'}, 403
        
        if facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Failed to delete review'}, 400

@api.route('/places/<place_id>')
class PlaceReviews(Resource):
    def get(self, place_id):
        """Get all reviews for a place"""
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
