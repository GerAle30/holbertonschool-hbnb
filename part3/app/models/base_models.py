from app import db
import uuid
from datetime import datetime


class BaseModel(db.Model):
    """Base model class that provides common attributes and methods for all entities.
    
    This abstract base class defines the common structure that all models inherit,
    including primary key, timestamps, and basic CRUD operations.
    """
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        """Initialize the BaseModel with optional keyword arguments.
        
        Args:
            **kwargs: Optional attributes to set on the model instance
        """
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    def save(self):
        """Save the current instance to the database and update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary.
        
        Args:
            data (dict): Dictionary containing attribute names and values to update
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at']:  # Prevent modification of immutable fields
                setattr(self, key, value)
        self.save()  # This will update the updated_at timestamp and commit to database

    def to_dict(self):
        """Convert the model instance to a dictionary representation.
        
        Returns:
            dict: Dictionary containing all model attributes
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            result[column.name] = value
        return result

    def __repr__(self):
        """Return a string representation of the model instance."""
        return f"<{self.__class__.__name__}(id='{self.id}')>"
