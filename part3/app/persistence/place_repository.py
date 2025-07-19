from app.models.place import Place
from app import db
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Place-specific repository that extends SQLAlchemyRepository with place domain operations.
    
    This repository encapsulates all place-related database operations and queries,
    providing specialized methods beyond basic CRUD operations for place management,
    location-based searches, and pricing queries.
    """
    
    def __init__(self):
        """Initialize the PlaceRepository with the Place model."""
        super().__init__(Place)
    
    def get_places_by_price_range(self, min_price, max_price):
        """Find places within a specific price range.
        
        Args:
            min_price (float): Minimum price per night
            max_price (float): Maximum price per night
            
        Returns:
            list: List of Place instances within the price range
        """
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()
    
    def get_places_by_location(self, latitude, longitude, radius_km=10):
        """Find places within a specific radius of given coordinates.
        
        Note: This is a simplified distance calculation. In production,
        you might want to use PostGIS or similar for accurate geo queries.
        
        Args:
            latitude (float): Center latitude
            longitude (float): Center longitude
            radius_km (float): Search radius in kilometers (default: 10)
            
        Returns:
            list: List of Place instances within the radius
        """
        # Approximate conversion: 1 degree ≈ 111 km
        degree_radius = radius_km / 111.0
        
        return self.model.query.filter(
            self.model.latitude >= latitude - degree_radius,
            self.model.latitude <= latitude + degree_radius,
            self.model.longitude >= longitude - degree_radius,
            self.model.longitude <= longitude + degree_radius
        ).all()
    
    def get_places_by_title_pattern(self, pattern):
        """Find places with titles matching a pattern (case-insensitive).
        
        Args:
            pattern (str): Pattern to search for in place titles
            
        Returns:
            list: List of matching Place instances
        """
        return self.model.query.filter(
            self.model.title.ilike(f'%{pattern}%')
        ).all()
    
    def get_places_above_price(self, min_price):
        """Get places with price above a certain threshold.
        
        Args:
            min_price (float): Minimum price threshold
            
        Returns:
            list: List of Place instances with price above threshold
        """
        return self.model.query.filter(self.model.price > min_price).all()
    
    def get_places_below_price(self, max_price):
        """Get places with price below a certain threshold.
        
        Args:
            max_price (float): Maximum price threshold
            
        Returns:
            list: List of Place instances with price below threshold
        """
        return self.model.query.filter(self.model.price < max_price).all()
    
    def get_recent_places(self, limit=10):
        """Get the most recently created places.
        
        Args:
            limit (int): Maximum number of places to return (default: 10)
            
        Returns:
            list: List of Place instances ordered by creation date (newest first)
        """
        return (self.model.query
                .order_by(self.model.created_at.desc())
                .limit(limit)
                .all())
    
    def get_places_ordered_by_price(self, ascending=True):
        """Get all places ordered by price.
        
        Args:
            ascending (bool): If True, order from lowest to highest price
            
        Returns:
            list: List of Place instances ordered by price
        """
        if ascending:
            return self.model.query.order_by(self.model.price.asc()).all()
        else:
            return self.model.query.order_by(self.model.price.desc()).all()
    
    def count_places(self):
        """Get the total count of places in the system.
        
        Returns:
            int: Total number of places
        """
        return self.model.query.count()
    
    def get_average_price(self):
        """Calculate the average price of all places.
        
        Returns:
            float: Average price per night, or 0 if no places exist
        """
        result = db.session.query(db.func.avg(self.model.price)).scalar()
        return float(result) if result is not None else 0.0
    
    def get_price_statistics(self):
        """Get comprehensive price statistics for all places.
        
        Returns:
            dict: Dictionary containing min, max, avg prices and place count
        """
        stats = db.session.query(
            db.func.min(self.model.price).label('min_price'),
            db.func.max(self.model.price).label('max_price'),
            db.func.avg(self.model.price).label('avg_price'),
            db.func.count(self.model.id).label('total_places')
        ).first()
        
        return {
            'min_price': float(stats.min_price) if stats.min_price else 0.0,
            'max_price': float(stats.max_price) if stats.max_price else 0.0,
            'avg_price': float(stats.avg_price) if stats.avg_price else 0.0,
            'total_places': int(stats.total_places)
        }
    
    def title_exists(self, title, exclude_id=None):
        """Check if a place with the given title already exists.
        
        Args:
            title (str): Title to check for existence
            exclude_id (str, optional): Place ID to exclude from check (for updates)
            
        Returns:
            bool: True if title exists, False otherwise
        """
        query = self.model.query.filter_by(title=title)
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        return query.first() is not None
    
    def soft_delete_place(self, place_id):
        """Soft delete a place by marking it as inactive.
        
        Note: This method assumes a future implementation of soft delete functionality.
        Currently performs a hard delete via the parent class.
        
        Args:
            place_id (str): ID of the place to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        # For now, perform hard delete. In future implementations,
        # this could set an 'is_active' flag to False instead
        return self.delete(place_id)
