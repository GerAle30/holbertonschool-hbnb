from app import db
from app.models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity model"""
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __init__(self, name):
        super().__init__()
        self.name = name
