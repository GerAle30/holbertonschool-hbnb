from app.models.reviews import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Review-specific repository that extends SQLAlchemyRepository with review domain operations.
    
    This repository encapsulates all review-related database operations and queries,
    providing specialized methods beyond basic CRUD operations for review management,
    rating analytics, and content filtering.
    """
    
    def __init__(self):
        """Initialize the ReviewRepository with the Review model."""
        super().__init__(Review)
    
    def get_reviews_by_rating(self, rating):
        """Find reviews with a specific rating.
        
        Args:
            rating (int): Rating value (1-5) to search for
            
        Returns:
            list: List of Review instances with the specified rating
        """
        return self.model.query.filter_by(rating=rating).all()
    
    def get_reviews_by_rating_range(self, min_rating, max_rating):
        """Find reviews within a specific rating range.
        
        Args:
            min_rating (int): Minimum rating (1-5)
            max_rating (int): Maximum rating (1-5)
            
        Returns:
            list: List of Review instances within the rating range
        """
        return self.model.query.filter(
            self.model.rating >= min_rating,
            self.model.rating <= max_rating
        ).all()
    
    def get_high_rated_reviews(self, min_rating=4):
        """Get reviews with high ratings.
        
        Args:
            min_rating (int): Minimum rating threshold (default: 4)
            
        Returns:
            list: List of Review instances with rating >= min_rating
        """
        return self.model.query.filter(self.model.rating >= min_rating).all()
    
    def get_low_rated_reviews(self, max_rating=2):
        """Get reviews with low ratings.
        
        Args:
            max_rating (int): Maximum rating threshold (default: 2)
            
        Returns:
            list: List of Review instances with rating <= max_rating
        """
        return self.model.query.filter(self.model.rating <= max_rating).all()
    
    def search_reviews_by_text(self, search_term):
        """Find reviews containing specific text (case-insensitive).
        
        Args:
            search_term (str): Text to search for in review content
            
        Returns:
            list: List of Review instances containing the search term
        """
        return self.model.query.filter(
            self.model.text.ilike(f'%{search_term}%')
        ).all()
    
    def get_recent_reviews(self, limit=10):
        """Get the most recently created reviews.
        
        Args:
            limit (int): Maximum number of reviews to return (default: 10)
            
        Returns:
            list: List of Review instances ordered by creation date (newest first)
        """
        return (self.model.query
                .order_by(self.model.created_at.desc())
                .limit(limit)
                .all())
    
    def get_reviews_ordered_by_rating(self, ascending=False):
        """Get all reviews ordered by rating.
        
        Args:
            ascending (bool): If True, order from lowest to highest rating
            
        Returns:
            list: List of Review instances ordered by rating
        """
        if ascending:
            return self.model.query.order_by(self.model.rating.asc()).all()
        else:
            return self.model.query.order_by(self.model.rating.desc()).all()
    
    def count_reviews(self):
        """Get the total count of reviews in the system.
        
        Returns:
            int: Total number of reviews
        """
        return self.model.query.count()
    
    def count_reviews_by_rating(self, rating):
        """Count reviews with a specific rating.
        
        Args:
            rating (int): Rating value to count
            
        Returns:
            int: Number of reviews with the specified rating
        """
        return self.model.query.filter_by(rating=rating).count()
    
    def get_average_rating(self):
        """Calculate the average rating of all reviews.
        
        Returns:
            float: Average rating, or 0 if no reviews exist
        """
        result = db.session.query(db.func.avg(self.model.rating)).scalar()
        return float(result) if result is not None else 0.0
    
    def get_rating_distribution(self):
        """Get the distribution of ratings across all reviews.
        
        Returns:
            dict: Dictionary with rating as key and count as value
        """
        distribution = {}
        for rating in range(1, 6):  # Ratings 1-5
            count = self.count_reviews_by_rating(rating)
            distribution[rating] = count
        return distribution
    
    def get_rating_statistics(self):
        """Get comprehensive rating statistics for all reviews.
        
        Returns:
            dict: Dictionary containing min, max, avg ratings and review count
        """
        stats = db.session.query(
            db.func.min(self.model.rating).label('min_rating'),
            db.func.max(self.model.rating).label('max_rating'),
            db.func.avg(self.model.rating).label('avg_rating'),
            db.func.count(self.model.id).label('total_reviews')
        ).first()
        
        return {
            'min_rating': int(stats.min_rating) if stats.min_rating else 0,
            'max_rating': int(stats.max_rating) if stats.max_rating else 0,
            'avg_rating': float(stats.avg_rating) if stats.avg_rating else 0.0,
            'total_reviews': int(stats.total_reviews),
            'distribution': self.get_rating_distribution()
        }
    
    def get_reviews_with_long_text(self, min_length=100):
        """Get reviews with text longer than specified length.
        
        Args:
            min_length (int): Minimum text length (default: 100)
            
        Returns:
            list: List of Review instances with long text content
        """
        return self.model.query.filter(
            db.func.length(self.model.text) >= min_length
        ).all()
    
    def get_reviews_with_short_text(self, max_length=50):
        """Get reviews with text shorter than specified length.
        
        Args:
            max_length (int): Maximum text length (default: 50)
            
        Returns:
            list: List of Review instances with short text content
        """
        return self.model.query.filter(
            db.func.length(self.model.text) <= max_length
        ).all()
    
    def update_review_text(self, review_id, new_text):
        """Update a review's text content with validation.
        
        Args:
            review_id (str): ID of the review to update
            new_text (str): New text content
            
        Returns:
            Review: Updated review instance, or None if not found
            
        Raises:
            ValueError: If new text is invalid
        """
        review = self.get(review_id)
        if not review:
            return None
        
        if not new_text or not new_text.strip():
            raise ValueError("Review text cannot be empty")
        
        review.text = new_text.strip()
        db.session.commit()
        return review
    
    def update_review_rating(self, review_id, new_rating):
        """Update a review's rating with validation.
        
        Args:
            review_id (str): ID of the review to update
            new_rating (int): New rating value (1-5)
            
        Returns:
            Review: Updated review instance, or None if not found
            
        Raises:
            ValueError: If new rating is invalid
        """
        review = self.get(review_id)
        if not review:
            return None
        
        try:
            rating_int = int(new_rating)
            if rating_int < 1 or rating_int > 5:
                raise ValueError("Rating must be between 1 and 5")
        except (TypeError, ValueError):
            raise ValueError("Rating must be a valid integer between 1 and 5")
        
        review.rating = rating_int
        db.session.commit()
        return review
    
    def soft_delete_review(self, review_id):
        """Soft delete a review by marking it as inactive.
        
        Note: This method assumes a future implementation of soft delete functionality.
        Currently performs a hard delete via the parent class.
        
        Args:
            review_id (str): ID of the review to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        # For now, perform hard delete. In future implementations,
        # this could set an 'is_active' flag to False instead
        return self.delete(review_id)
