from app import db
from .base_models import BaseModel
from sqlalchemy.orm import relationship


class Review(BaseModel):
    """Review model for managing user reviews of places.
    
    This model handles user reviews including ratings and text comments
    for rental properties.
    """
    __tablename__ = 'reviews'
    
    # Column definitions with appropriate constraints
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='reviews')
    place = relationship('Place', back_populates='reviews')

    def __init__(self, text=None, rating=None, user_id=None, place_id=None, **kwargs):
        """Initialize a new Review instance with validation.
        
        Args:
            text (str): Text content of the review (required)
            rating (int): Rating from 1 to 5 (required)
            user_id (str): ID of the user creating the review (required)
            place_id (str): ID of the place being reviewed (required)
            **kwargs: Additional keyword arguments passed to BaseModel
        
        Raises:
            ValueError: If validation fails for any required field
        """
        # Validate input parameters
        if text is not None:
            if not text or not text.strip():
                raise ValueError("Review text is required and cannot be empty")
        
        if rating is not None:
            try:
                rating_int = int(rating)
                if rating_int < 1 or rating_int > 5:
                    raise ValueError("Rating must be an integer between 1 and 5")
            except (TypeError, ValueError):
                raise ValueError("Rating must be a valid integer between 1 and 5")
        
        # Call parent constructor
        super().__init__(**kwargs)
        
        # Set attributes
        if text is not None:
            self.text = text.strip()
        if rating is not None:
            self.rating = int(rating)
        if user_id is not None:
            self.user_id = user_id
        if place_id is not None:
            self.place_id = place_id
    
    def __repr__(self):
        """Return string representation of Review instance."""
        return f"<Review(id='{self.id}', rating={self.rating})>"
