# Administrator Permissions Implementation

This document describes the implementation of administrator permissions in the HBnB API.

## Overview

Administrator permissions have been implemented to restrict certain operations to users with admin privileges. The system uses JWT tokens with an `is_admin` flag to determine user permissions.

## Admin-Restricted Endpoints

The following endpoints are now restricted to administrators only:

### 1. User Management
- **POST /api/v1/users/**: Create a new user (Admin only)
- **PUT /api/v1/users/<user_id>**: Modify user details including email, password, and admin status (Admin bypass for ownership)

### 2. Amenity Management  
- **POST /api/v1/amenities/**: Add a new amenity (Admin only)
- **PUT /api/v1/amenities/<amenity_id>**: Modify amenity details (Admin only)

### 3. Admin Bypass for Ownership Restrictions
Administrators can bypass ownership restrictions on:
- **Places**: Modify or delete any place regardless of ownership
- **Reviews**: Modify or delete any review regardless of ownership

## Implementation Details

### User Model
The `User` model already includes an `is_admin` field:
```python
class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        # ... existing code ...
        self.is_admin = is_admin
```

### JWT Token
JWT tokens include the `is_admin` flag:
```python
access_token = create_access_token(identity={
    'id': str(user.id), 
    'is_admin': user.is_admin
})
```

### Permission Checks
Admin permission checks are implemented using:
```python
current_user = get_jwt_identity()
is_admin = current_user.get('is_admin', False)

if not is_admin:
    return {'error': 'Admin access required'}, 403
```

### Ownership Bypass
For places and reviews, admins can bypass ownership restrictions:
```python
if existing_resource.owner.id != current_user['id'] and not is_admin:
    return {'error': 'Unauthorized action.'}, 403
```

## API Changes Summary

### Users API (`/api/v1/users/`)
- **POST**: Now requires admin authentication (`@jwt_required()`)
- **PUT**: Admins can modify email, password, and admin status; regular users limited to first_name/last_name

### Amenities API (`/api/v1/amenities/`)
- **POST**: Now requires admin authentication (`@jwt_required()`)  
- **PUT**: Now requires admin authentication (`@jwt_required()`)

### Places API (`/api/v1/places/`)
- **PUT**: Admins can modify any place (ownership bypass)
- **DELETE**: New endpoint added; admins can delete any place

### Reviews API (`/api/v1/reviews/`)
- **PUT**: Admins can modify any review (ownership bypass)
- **DELETE**: Admins can delete any review (ownership bypass)

## Error Responses

### 403 Forbidden - Admin Access Required
```json
{
    "error": "Admin access required to create users"
}
```

### 403 Forbidden - Unauthorized Action  
```json
{
    "error": "Unauthorized action."
}
```

### 400 Bad Request - Restricted Fields
```json
{
    "error": "You cannot modify email or password."
}
```

## Security Considerations

1. **Admin User Creation**: Since user creation requires admin privileges, initial admin setup needs special consideration
2. **Token Security**: JWT tokens contain admin status and should be protected
3. **Admin Privilege Escalation**: Only existing admins can grant admin privileges to other users
4. **Audit Trail**: Consider implementing logging for admin actions

## Initial Setup

Since user creation now requires admin privileges, you need to set up an initial admin user. Options include:

1. **Temporary bypass**: Temporarily remove admin restriction, create admin user, then re-enable
2. **Database seeding**: Manually insert admin user into data store  
3. **Configuration flag**: Add environment variable to allow initial admin creation
4. **Migration script**: Create a one-time setup script

## Testing

Use the provided `test_admin_permissions.py` script to verify the implementation:

```bash
python test_admin_permissions.py
```

This script tests:
- Admin-only user creation
- Admin-only amenity creation/modification  
- Admin bypass of ownership restrictions
- Regular user permission limitations

## Migration Notes

When deploying this update:

1. Ensure you have at least one admin user created before enabling restrictions
2. Update client applications to handle 403 responses for restricted operations
3. Update API documentation to reflect new permission requirements
4. Test all admin operations before going live

## Files Modified

- `app/api/v1/user.py`: Added admin restrictions and permissions
- `app/api/v1/amenities.py`: Added admin restrictions  
- `app/api/v1/places.py`: Added DELETE endpoint and admin bypass
- `app/api/v1/reviews.py`: Already had admin bypass implemented
- `app/services/facade.py`: Added `delete_place` method and improved user updates
- `test_admin_permissions.py`: Comprehensive test suite
- `ADMIN_PERMISSIONS.md`: This documentation file
