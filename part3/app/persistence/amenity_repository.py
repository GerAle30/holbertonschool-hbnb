from app.models.amenities import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Amenity-specific repository that extends SQLAlchemyRepository with amenity domain operations.
    
    This repository encapsulates all amenity-related database operations and queries,
    providing specialized methods beyond basic CRUD operations for amenity management,
    uniqueness validation, and availability checks.
    """
    
    def __init__(self):
        """Initialize the AmenityRepository with the Amenity model."""
        super().__init__(Amenity)
    
    def name_exists(self, name, exclude_id=None):
        """Check if an amenity with the given name already exists.
        
        Args:
            name (str): Name to check for existence
            exclude_id (str, optional): Amenity ID to exclude from check (for updates)
            
        Returns:
            bool: True if name exists, False otherwise
        """
        query = self.model.query.filter_by(name=name)
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        return query.first() is not None
    
    def get_amenities_ordered_by_name(self, ascending=True):
        """Get all amenities ordered by name.
        
        Args:
            ascending (bool): If True, order from A to Z
            
        Returns:
            list: List of Amenity instances ordered by name
        """
        if ascending:
            return self.model.query.order_by(self.model.name.asc()).all()
        else:
            return self.model.query.order_by(self.model.name.desc()).all()
    
    def count_amenities(self):
        """Get the total count of amenities in the system.
        
        Returns:
            int: Total number of amenities
        """
        return self.model.query.count()
    
    def get_unique_amenities(self, limit=10):
        """Get a list of unique amenity names.
        
        Args:
            limit (int): Maximum number of amenities to return (default: 10)
            
        Returns:
            list: List of unique amenity names
        """
        return [amenity.name for amenity in self.model.query.distinct(self.model.name).limit(limit).all()]
    
    def get_recent_amenities(self, limit=10):
        """Get the most recently created amenities.
        
        Args:
            limit (int): Maximum number of amenities to return (default: 10)
            
        Returns:
            list: List of Amenity instances ordered by creation date (newest first)
        """
        return (self.model.query
                .order_by(self.model.created_at.desc())
                .limit(limit)
                .all())
    
    def soft_delete_amenity(self, amenity_id):
        """Soft delete an amenity by marking it as inactive.
        
        Note: This method assumes a future implementation of soft delete functionality.
        Currently performs a hard delete via the parent class.
        
        Args:
            amenity_id (str): ID of the amenity to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        # For now, perform hard delete. In future implementations,
        # this could set an 'is_active' flag to False instead
        return self.delete(amenity_id)
