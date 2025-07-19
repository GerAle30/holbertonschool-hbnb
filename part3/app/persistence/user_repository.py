from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """User-specific repository that extends SQLAlchemyRepository with user domain operations.
    
    This repository encapsulates all user-related database operations and queries,
    providing specialized methods beyond basic CRUD operations for user management,
    authentication, and authorization.
    """
    
    def __init__(self):
        """Initialize the UserRepository with the User model."""
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """Find a user by their email address.
        
        This method is essential for authentication and user lookup operations.
        Since email is unique in the database, this returns a single user or None.
        
        Args:
            email (str): The email address to search for
            
        Returns:
            User: User instance if found, None otherwise
        """
        if not email:
            return None
        return self.model.query.filter_by(email=email).first()
    
    def email_exists(self, email):
        """Check if an email address is already registered.
        
        Useful for registration validation and preventing duplicate accounts.
        
        Args:
            email (str): Email address to check
            
        Returns:
            bool: True if email exists, False otherwise
        """
        if not email:
            return False
        return self.model.query.filter_by(email=email).first() is not None
    
    def get_all_admins(self):
        """Retrieve all users with admin privileges.
        
        Useful for admin management and authorization operations.
        
        Returns:
            list: List of User instances with is_admin=True
        """
        return self.model.query.filter_by(is_admin=True).all()
    
    def get_users_by_name(self, first_name=None, last_name=None):
        """Find users by first name, last name, or both.
        
        Supports flexible user search functionality.
        
        Args:
            first_name (str, optional): First name to search for
            last_name (str, optional): Last name to search for
            
        Returns:
            list: List of matching User instances
        """
        query = self.model.query
        
        if first_name:
            query = query.filter(self.model.first_name.ilike(f'%{first_name}%'))
        
        if last_name:
            query = query.filter(self.model.last_name.ilike(f'%{last_name}%'))
        
        return query.all()
    
    def update_password(self, user_id, new_password):
        """Update a user's password with proper hashing.
        
        Encapsulates the password update logic with automatic hashing.
        
        Args:
            user_id (str): ID of the user to update
            new_password (str): New plain text password
            
        Returns:
            User: Updated user instance, or None if user not found
            
        Raises:
            ValueError: If password is invalid
        """
        user = self.get(user_id)
        if not user:
            return None
        
        if not new_password:
            raise ValueError("Password cannot be empty")
        
        user.hash_password(new_password)
        db.session.commit()
        return user
    
    def toggle_admin_status(self, user_id):
        """Toggle a user's admin status.
        
        Useful for admin management operations.
        
        Args:
            user_id (str): ID of the user to toggle
            
        Returns:
            User: Updated user instance with toggled admin status, or None if not found
        """
        user = self.get(user_id)
        if not user:
            return None
        
        user.is_admin = not user.is_admin
        db.session.commit()
        return user
    
    def authenticate_user(self, email, password):
        """Authenticate a user with email and password.
        
        Combines user lookup and password verification in one operation.
        
        Args:
            email (str): User's email address
            password (str): Plain text password to verify
            
        Returns:
            User: User instance if authentication successful, None otherwise
        """
        if not email or not password:
            return None
        
        user = self.get_user_by_email(email)
        if user and user.verify_password(password):
            return user
        
        return None
    
    def get_recent_users(self, limit=10):
        """Get the most recently created users.
        
        Useful for admin dashboards and user management interfaces.
        
        Args:
            limit (int): Maximum number of users to return (default: 10)
            
        Returns:
            list: List of User instances ordered by creation date (newest first)
        """
        return (self.model.query
                .order_by(self.model.created_at.desc())
                .limit(limit)
                .all())
    
    def count_users(self):
        """Get the total count of users in the system.
        
        Useful for statistics and dashboard metrics.
        
        Returns:
            int: Total number of users
        """
        return self.model.query.count()
    
    def count_admin_users(self):
        """Get the count of admin users in the system.
        
        Useful for admin management and security auditing.
        
        Returns:
            int: Number of admin users
        """
        return self.model.query.filter_by(is_admin=True).count()
    
    def soft_delete_user(self, user_id):
        """Soft delete a user by marking them as inactive.
        
        Note: This method assumes a future implementation of soft delete functionality.
        Currently performs a hard delete via the parent class.
        
        Args:
            user_id (str): ID of the user to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        # For now, perform hard delete. In future implementations,
        # this could set an 'is_active' flag to False instead
        return self.delete(user_id)
