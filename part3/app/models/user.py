from app import db, bcrypt
from app.models.base_models import BaseModel
from sqlalchemy.orm import relationship
import re


class User(BaseModel):
    """User model for managing user accounts and authentication.
    
    This model handles user registration, authentication, and profile management.
    It includes validation for email format and password hashing for security.
    """
    __tablename__ = 'users'
    
    # Email validation regex pattern
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    
    # Column definitions with appropriate constraints
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    places = relationship('Place', back_populates='owner', lazy=True)
    reviews = relationship('Review', back_populates='user', lazy=True)

    def __init__(self, first_name=None, last_name=None, email=None, is_admin=False, **kwargs):
        """Initialize a new User instance with validation.
        
        Args:
            first_name (str): User's first name (required, max 50 chars)
            last_name (str): User's last name (required, max 50 chars) 
            email (str): User's email address (required, must be valid format)
            is_admin (bool): Whether user has admin privileges (default: False)
            **kwargs: Additional keyword arguments passed to BaseModel
        
        Raises:
            ValueError: If validation fails for any required field
        """
        # Validate input parameters
        if first_name is not None:
            if not first_name or len(first_name) > 50:
                raise ValueError(
                    "First name is required and must be <= 50 characters.")
        
        if last_name is not None:
            if not last_name or len(last_name) > 50:
                raise ValueError(
                    "Last name is required and must be <= 50 characters.")
        
        if email is not None:
            if not email or not re.match(self.EMAIL_REGEX, email):
                raise ValueError("A valid email is required.")
        
        # Call parent constructor
        super().__init__(**kwargs)
        
        # Set attributes
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email
        self.is_admin = is_admin
        
        # Password will be set via hash_password method
        if not hasattr(self, 'password') or self.password is None:
            self.password = ''  # Temporary placeholder, should be set via hash_password

    def hash_password(self, password):
        """Hash the password before storing it.
        
        Args:
            password (str): Plain text password to hash
        
        Raises:
            ValueError: If password is empty or None
        """
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        if not password or not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        """Convert User instance to dictionary, excluding sensitive data.
        
        Returns:
            dict: User data dictionary without password field
        """
        user_dict = super().to_dict()
        # Remove password from dictionary representation for security
        user_dict.pop('password', None)
        return user_dict
    
    def __repr__(self):
        """Return string representation of User instance."""
        return f"<User(id='{self.id}', email='{self.email}', admin={self.is_admin})>"
