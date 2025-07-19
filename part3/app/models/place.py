from app import db
from .base_models import BaseModel
from sqlalchemy.orm import relationship


class Place(BaseModel):
    """Place model for managing rental place listings.
    
    This model handles place information including location, pricing,
    and descriptive details for rental properties.
    """
    __tablename__ = 'places'
    
    # Column definitions with appropriate constraints
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = relationship('User', back_populates='places')
    amenities = relationship('Amenity', secondary='place_amenities', back_populates='places')
    reviews = relationship('Review', back_populates='place')

    def __init__(self, title=None, description=None, price=None, 
                 latitude=None, longitude=None, owner_id=None, **kwargs):
        """Initialize a new Place instance with validation.
        
        Args:
            title (str): Title of the place (required)
            description (str): Description of the place (optional)
            price (float): Price per night (required, must be positive)
            latitude (float): Latitude coordinate (required, -90 to 90)
            longitude (float): Longitude coordinate (required, -180 to 180)
            owner_id (str): ID of the place owner (required)
            **kwargs: Additional keyword arguments passed to BaseModel
        
        Raises:
            ValueError: If validation fails for any required field
        """
        # Validate input parameters
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Title is required and cannot be empty")
            if len(title.strip()) > 100:
                raise ValueError("Title must be 100 characters or less")
        
        if price is not None:
            try:
                price_float = float(price)
                if price_float <= 0:
                    raise ValueError("Price must be a positive number")
            except (TypeError, ValueError):
                raise ValueError("Price must be a valid positive number")
        
        if latitude is not None:
            try:
                lat_float = float(latitude)
                if lat_float < -90 or lat_float > 90:
                    raise ValueError("Latitude must be between -90 and 90")
            except (TypeError, ValueError):
                raise ValueError("Latitude must be a valid number")
        
        if longitude is not None:
            try:
                lon_float = float(longitude)
                if lon_float < -180 or lon_float > 180:
                    raise ValueError("Longitude must be between -180 and 180")
            except (TypeError, ValueError):
                raise ValueError("Longitude must be a valid number")
        
        # Call parent constructor
        super().__init__(**kwargs)
        
        # Set attributes
        if title is not None:
            self.title = title.strip()
        if description is not None:
            self.description = description
        if price is not None:
            self.price = float(price)
        if latitude is not None:
            self.latitude = float(latitude)
        if longitude is not None:
            self.longitude = float(longitude)
        if owner_id is not None:
            self.owner_id = owner_id
    
    def __repr__(self):
        """Return string representation of Place instance."""
        return f"<Place(id='{self.id}', title='{self.title}', price={self.price})>"
