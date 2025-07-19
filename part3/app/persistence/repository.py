from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values()
                    if getattr(obj, attr_name) == attr_value), None)


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the Repository interface.
    
    This repository provides database CRUD operations using SQLAlchemy ORM.
    It's designed to be flexible and reusable for different entities.
    """
    
    def __init__(self, model):
        """Initialize the repository with a SQLAlchemy model.
        
        Args:
            model: SQLAlchemy model class (e.g., User, Place, Review)
        """
        self.model = model

    def add(self, obj):
        """Add a new object to the database.
        
        Args:
            obj: Model instance to add to the database
        """
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Retrieve an object by its ID.
        
        Args:
            obj_id: The ID of the object to retrieve
            
        Returns:
            Model instance or None if not found
        """
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all objects of this model type.
        
        Returns:
            List of all model instances
        """
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with new data.
        
        Args:
            obj_id: The ID of the object to update
            data: Dictionary of attributes to update
            
        Returns:
            Updated model instance or None if not found
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        """Delete an object from the database.
        
        Args:
            obj_id: The ID of the object to delete
            
        Returns:
            True if deleted, False if object not found
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Find the first object with a specific attribute value.
        
        Args:
            attr_name: Name of the attribute to search by
            attr_value: Value to match
            
        Returns:
            First matching model instance or None if not found
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
