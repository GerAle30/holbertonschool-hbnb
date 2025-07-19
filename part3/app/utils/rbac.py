"""
Role-Based Access Control (RBAC) utilities and decorators
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required

def admin_required(f):
    """
    Decorator that requires admin privileges.
    Must be used after @jwt_required()
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        jwt_claims = get_jwt()
        
        # Check if user has admin privileges
        is_admin = current_user.get('is_admin', False) or jwt_claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        return f(*args, **kwargs)
    return decorated_function

def check_admin_or_owner(resource_owner_id):
    """
    Check if current user is admin or owner of resource
    Returns: (is_authorized, current_user, is_admin)
    """
    current_user = get_jwt_identity()
    jwt_claims = get_jwt()
    
    is_admin = current_user.get('is_admin', False) or jwt_claims.get('is_admin', False)
    is_owner = current_user.get('id') == resource_owner_id
    
    is_authorized = is_admin or is_owner
    
    return is_authorized, current_user, is_admin

def get_current_user_info():
    """
    Get comprehensive current user information from JWT
    Returns: dict with user_id, is_admin, and other claims
    """
    current_user = get_jwt_identity()
    jwt_claims = get_jwt()
    
    return {
        'user_id': current_user.get('id'),
        'is_admin': current_user.get('is_admin', False) or jwt_claims.get('is_admin', False),
        'identity': current_user,
        'claims': jwt_claims
    }

class RBACError(Exception):
    """Custom exception for RBAC-related errors"""
    pass

def require_admin_or_owner(resource_owner_id, error_message="Access denied"):
    """
    Raise exception if user is not admin or owner
    """
    is_authorized, current_user, is_admin = check_admin_or_owner(resource_owner_id)
    
    if not is_authorized:
        raise RBACError(error_message)
    
    return current_user, is_admin
