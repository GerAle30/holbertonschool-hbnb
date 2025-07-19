# Admin Endpoints Testing Guide

## Overview

This guide addresses the **"Unauthorized action"** problem when testing admin endpoints and provides multiple strategies to create and test admin users.

## The Bootstrap Problem

Admin endpoints require admin privileges to test, but creating admin users also requires admin privileges. This creates a chicken-and-egg problem that needs to be solved.

## Solution Strategies

### Strategy 1: Database Direct Insert (Recommended for Production)

Connect directly to your database and insert an admin user:

```sql
-- For PostgreSQL
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    gen_random_uuid(),  -- Or use uuid_generate_v4()
    'System',
    'Administrator',
    'admin@example.com',
    '$2b$12$...',  -- Use proper bcrypt hash
    true,
    NOW(),
    NOW()
);

-- For SQLite
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'System',
    'Administrator',
    'admin@example.com',
    'hashed_password_here',
    1,  -- SQLite uses 1 for true
    datetime('now'),
    datetime('now')
);
```

**Admin Credentials:**
- Email: `admin@example.com`
- Password: `admin123` (hash this properly)

### Strategy 2: Application Code Auto-Creation (Recommended for Development)

Add this code to your application startup (e.g., `app/__init__.py`):

```python
def ensure_admin_user_exists():
    """Ensure at least one admin user exists in the system"""
    from app.services import facade
    
    admin_email = "admin@example.com"
    admin_password = "admin123"
    
    # Check if admin user already exists
    existing_admin = facade.get_user_by_email(admin_email)
    if existing_admin:
        if not existing_admin.is_admin:
            # Promote existing user to admin
            facade.update_user(existing_admin.id, {'is_admin': True})
            print(f"Promoted user to admin: {admin_email}")
        return existing_admin
    
    # Create admin user
    try:
        admin_user_data = {
            'first_name': 'System',
            'last_name': 'Administrator',
            'email': admin_email,
            'password': admin_password,
            'is_admin': True  # This is the key flag!
        }
        
        admin_user = facade.create_user(admin_user_data)
        print(f"Created admin user: {admin_email}")
        return admin_user
        
    except Exception as e:
        print(f"Failed to create admin user: {e}")
        return None

# Call this function when your app starts
if __name__ == "__main__":
    ensure_admin_user_exists()
```

### Strategy 3: Environment Variables

Set environment variables:

```bash
export ADMIN_EMAIL="admin@example.com"
export ADMIN_PASSWORD="admin123"
export AUTO_CREATE_ADMIN="true"
```

Add to your application:

```python
import os
from app.services import facade

def setup_admin_from_env():
    """Create admin user from environment variables"""
    if os.getenv('AUTO_CREATE_ADMIN', 'false').lower() == 'true':
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        if not facade.get_user_by_email(admin_email):
            admin_data = {
                'first_name': 'Environment',
                'last_name': 'Admin',
                'email': admin_email,
                'password': admin_password,
                'is_admin': True
            }
            
            admin = facade.create_user(admin_data)
            print(f"Created admin from environment: {admin_email}")
```

## Testing Admin Endpoints

### Step 1: Start Your API Server

```bash
# Make sure your Flask/API server is running
python app.py  # or however you start your server
# Server should be accessible at http://127.0.0.1:5000
```

### Step 2: Get Admin Token

```bash
# Login as admin user
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -d '{"email": "admin@example.com", "password": "admin123"}' \
  -H "Content-Type: application/json"

# Response should contain:
# {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."}
```

**Save the token for subsequent requests:**
```bash
export ADMIN_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOi..."
```

### Step 3: Verify Admin Status

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/auth/protected" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Should return:
# {
#   "message": "Hello, user <user_id>",
#   "user_id": "<user_id>", 
#   "is_admin": true
# }
```

## Admin Endpoint Tests

### Test 1: Create a New User as an Admin

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -d '{
    "email": "newuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "testpass123"
  }' \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json"
```

**Expected Response (201):**
```json
{
  "id": "user_id",
  "first_name": "Test",
  "last_name": "User", 
  "email": "newuser@example.com",
  "is_admin": false,
  "message": "User successfully created"
}
```

### Test 2: Modify Another User's Data as an Admin

```bash
# Get the user_id from the previous response
export USER_ID="user_id_from_previous_response"

curl -X PUT "http://127.0.0.1:5000/api/v1/users/$USER_ID" \
  -d '{
    "email": "updatedemail@example.com",
    "first_name": "Updated",
    "last_name": "TestUser"
  }' \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json"
```

**Expected Response (200):**
```json
{
  "id": "user_id",
  "first_name": "Updated",
  "last_name": "TestUser",
  "email": "updatedemail@example.com", 
  "is_admin": false,
  "message": "User successfully modified by administrator",
  "modified_by_admin": true
}
```

### Test 3: Add a New Amenity as an Admin

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -d '{"name": "Swimming Pool"}' \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json"
```

**Expected Response (201):**
```json
{
  "id": "amenity_id",
  "name": "Swimming Pool",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00",
  "message": "Amenity successfully created by administrator",
  "created_by_admin": true
}
```

### Test 4: Modify an Amenity as an Admin

```bash
# Get the amenity_id from the previous response
export AMENITY_ID="amenity_id_from_previous_response"

curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID" \
  -d '{"name": "Updated Swimming Pool"}' \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json"
```

**Expected Response (200):**
```json
{
  "id": "amenity_id",
  "name": "Updated Swimming Pool",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:05:00", 
  "message": "Amenity successfully modified by administrator",
  "modified_by_admin": true
}
```

### Test 5: Admin Bypass - Modify Another User's Place

```bash
# First, create a regular user and have them create a place
# Then admin can modify it

curl -X PUT "http://127.0.0.1:5000/api/v1/places/<place_id>" \
  -d '{
    "title": "Modified by Admin",
    "price": 500.0
  }' \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json"
```

**Expected Response (200):**
```json
{
  "id": "place_id",
  "title": "Modified by Admin",
  "price": 500.0,
  "owner": {
    "id": "original_owner_id",
    "first_name": "Original",
    "last_name": "Owner"
  },
  "message": "Place successfully modified by administrator",
  "modified_by_admin": true
}
```

## Error Responses

### Unauthorized Access (403)
```json
{
  "error": "Admin privileges required"
}
```

### Invalid Token (401)
```json
{
  "error": "Invalid credentials"
}
```

### Resource Not Found (404)
```json
{
  "error": "User not found"
}
```

### Validation Error (400)
```json
{
  "error": "Email already registered"
}
```

## Automated Testing

Use the provided test scripts:

```bash
# Setup admin user
python3 setup_admin_user.py

# Run comprehensive admin endpoint tests
python3 test_admin_endpoints.py

# Test specific admin bypass functionality
python3 test_admin_bypass_ownership.py
```

## Key Features Verified

- **Admin User Creation**: Only admins can create new users  
- **Admin User Modification**: Admins can modify any user's data  
- **Admin Amenity Management**: Full CRUD operations for amenities  
- **Admin Ownership Bypass**: Modify/delete resources owned by others  
- **Enhanced JWT Verification**: Uses `get_jwt()` for comprehensive checking  
- **Admin Action Tracking**: Responses include admin modification flags  
- **Proper Error Handling**: Clear error messages and appropriate status codes

## Security Notes

- Admin users have elevated privileges - protect admin credentials carefully
- JWT tokens contain `is_admin` flag for authorization
- Original resource ownership is preserved after admin modifications
- Admin actions are tracked in API responses for audit purposes
- Regular users cannot escalate their own privileges

## Troubleshooting

1. **Connection Refused**: Ensure API server is running on `http://127.0.0.1:5000`
2. **No Admin User**: Use one of the setup strategies above
3. **Token Issues**: Verify JWT token contains `is_admin: true`
4. **Permission Denied**: Check that user account has `is_admin: true` in database
