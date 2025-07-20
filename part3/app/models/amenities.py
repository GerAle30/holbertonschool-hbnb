from app import db
from .base_models import BaseModel
from sqlalchemy.orm import relationship

# Association table for many-to-many relationship between Place and Amenity
place_amenities = db.Table('place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(BaseModel):
    """Amenity model for managing place amenities.
    
    This model handles amenity information that can be associated
    with rental places (e.g., WiFi, Pool, Parking).
    """
    __tablename__ = 'amenities'
    
    # Column definitions with appropriate constraints
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Relationships
    places = relationship('Place', secondary='place_amenities', back_populates='amenities', lazy='subquery')

    def __init__(self, name=None, **kwargs):
        """Initialize a new Amenity instance with validation.
        
        Args:
            name (str): Name of the amenity (required, max 50 chars, unique)
            **kwargs: Additional keyword arguments passed to BaseModel
        
        Raises:
            ValueError: If validation fails for any required field
        """
        # Validate input parameters
        if name is not None:
            if not name or not name.strip():
                raise ValueError("Amenity name is required and cannot be empty")
            if len(name.strip()) > 50:
                raise ValueError("Amenity name must be 50 characters or less")
        
        # Call parent constructor
        super().__init__(**kwargs)
        
        # Set attributes
        if name is not None:
            self.name = name.strip()
    
    def __repr__(self):
        """Return string representation of Amenity instance."""
        return f"<Amenity(id='{self.id}', name='{self.name}')>"
