"""
Example SQLAlchemy model to demonstrate database functionality
This file demonstrates how to create SQLAlchemy models in the project
"""

from app import db
from datetime import datetime


class ExampleModel(db.Model):
    """Example model to test SQLAlchemy functionality"""
    
    __tablename__ = 'example'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExampleModel {self.name}>'
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
