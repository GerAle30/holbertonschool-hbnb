# Secured Endpoints with JWT Authentication

This document outlines the JWT-protected endpoints and their authorization rules.

## Authentication Required Endpoints

All the following endpoints require a valid JWT token in the `Authorization` header:
```
Authorization: Bearer <jwt_token>
```

## Endpoint Security Implementation

### 1. **POST /api/v1/places/** - Create a new place
- **Authentication**: JWT required
- **Authorization**: 
  - Users can only create places for themselves
  - Admins can create places for any user
- **Validation**: `owner_id` must match current user's ID (unless admin)

### 2. **PUT /api/v1/places/<place_id>** - Update place details
- **Authentication**: JWT required
- **Authorization**: 
  - Only the place owner can modify their place
  - Admins can modify any place
- **Security**: Ownership verification before allowing updates

### 3. **POST /api/v1/reviews/** - Create a new review
- **Authentication**: JWT required
- **Authorization**: 
  - Users cannot review their own places
  - Users can only create one review per place
  - Users can only create reviews under their own user ID
- **Business Logic**:
  - Validates place exists
  - Prevents duplicate reviews from same user
  - Prevents self-reviewing

### 4. **PUT /api/v1/reviews/<review_id>** - Update review
- **Authentication**: JWT required
- **Authorization**: 
  - Users can only modify their own reviews
  - Admins can modify any review
- **Security**: 
  - Prevents changing review ownership (user_id)
  - Prevents changing review place (place_id)

### 5. **DELETE /api/v1/reviews/<review_id>** - Delete review
- **Authentication**: JWT required
- **Authorization**: 
  - Users can only delete their own reviews
  - Admins can delete any review
- **Security**: Ownership verification before deletion

### 6. **PUT /api/v1/users/<user_id>** - Modify user information
- **Authentication**: JWT required
- **Authorization**: 
  - Users can only modify their own profile
  - Admins can modify any user profile
- **Restrictions**: 
  - Only `first_name` and `last_name` can be updated
  - Email and password cannot be modified through this endpoint
- **Security**: Field validation prevents unauthorized data changes

## Authorization Patterns

### User Ownership Pattern
```python
# Check if current user owns the resource
if resource.owner.id != current_user['id'] and not current_user.get('is_admin', False):
    return {'error': 'Unauthorized'}, 403
```

### Admin Override Pattern
```python
# Allow admins to perform actions on any resource
if not current_user.get('is_admin', False):
    # Apply user-level restrictions
```

### Field Restriction Pattern
```python
# Validate only allowed fields are being updated
allowed_fields = {'first_name', 'last_name'}
invalid_fields = set(user_data.keys()) - allowed_fields
if invalid_fields:
    return {'error': 'Invalid fields'}, 400
```

## Error Responses

### 401 - Unauthorized
- Missing or invalid JWT token
- Token expired

### 403 - Forbidden
- Valid token but insufficient permissions
- Attempting to access/modify another user's resources
- Business rule violations (e.g., reviewing own place)

### 404 - Not Found
- Resource doesn't exist
- Required related resources not found

### 400 - Bad Request
- Invalid input data
- Attempting to update restricted fields
- Business rule violations

## Security Features

1. **JWT Token Validation**: All protected endpoints validate JWT tokens
2. **User Identity Extraction**: `get_jwt_identity()` provides user context
3. **Ownership Verification**: Resources can only be modified by owners
4. **Admin Privileges**: Admins can override ownership restrictions
5. **Field-level Security**: Restricted fields cannot be updated
6. **Business Rule Enforcement**: Prevents invalid operations (self-reviews, etc.)
7. **Comprehensive Error Handling**: Clear error messages for security violations

## Testing the Secured Endpoints

### 1. Login to get JWT token:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

### 2. Use token in subsequent requests:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt_token>" \
  -d '{"title": "My Place", "price": 100, ...}'
```

The security implementation ensures that users can only access and modify their own resources while providing administrators with the ability to manage all resources in the system.
