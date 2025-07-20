# Manual cURL Tests for SQLAlchemy Relationships

This document provides the manual cURL commands to test all four SQLAlchemy relationships.

## Prerequisites

1. Start the Flask server:
```bash
cd /home/alejandro/holbertonschool-hbnb/part3
flask run --host=0.0.0.0 --port=5000
```

2. Initialize the database (run this Python script first):
```python
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    db.create_all()
    
    # Create admin user
    admin = User(first_name="Admin", last_name="User", email="admin@test.com", is_admin=True)
    admin.hash_password("admin123")
    db.session.add(admin)
    
    # Create regular user
    user = User(first_name="Test", last_name="User", email="user@test.com", is_admin=False)
    user.hash_password("user123")
    db.session.add(user)
    
    db.session.commit()
    print("Database initialized")
```

## Step-by-Step Testing

### 1. Authentication

**Admin Login:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@test.com", "password": "admin123"}'
```

**Regular User Login:**
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@test.com", "password": "user123"}'
```

Save the `access_token` from the responses for use in subsequent requests.

### 2. Create Amenities (for Many-to-Many testing)

```bash
# Create WiFi amenity (admin only)
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{"name": "WiFi"}'

# Create Swimming Pool amenity
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{"name": "Swimming Pool"}'

# Create Parking amenity
curl -X POST http://localhost:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{"name": "Parking"}'
```

### 3. Test User-Place Relationship (One-to-Many)

**Create Place as Admin:**
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{
    "title": "Modern Apartment",
    "description": "Beautiful apartment in downtown", 
    "price": 150.0,
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

**Create Place as Regular User:**
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -d '{
    "title": "Cozy Cabin",
    "description": "Mountain cabin retreat",
    "price": 120.0,
    "latitude": 39.5501,
    "longitude": -105.7821
  }'
```

**Retrieve All Places (verify ownership):**
```bash
curl -X GET http://localhost:5000/api/v1/places/
```

### 4. Test User-Review and Place-Review Relationships (One-to-Many)

**Create Review (Regular User reviews Admin's Place):**
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -d '{
    "text": "Excellent place! Very clean and comfortable.",
    "rating": 5,
    "user_id": "REGULAR_USER_ID",
    "place_id": "ADMIN_PLACE_ID"
  }'
```

**Create Review (Admin reviews Regular User's Place):**
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -d '{
    "text": "Great cabin but a bit remote.",
    "rating": 4,
    "user_id": "ADMIN_USER_ID", 
    "place_id": "USER_PLACE_ID"
  }'
```

**Retrieve All Reviews:**
```bash
curl -X GET http://localhost:5000/api/v1/reviews/
```

### 5. Verify Relationships

**Get Specific Place with Owner and Reviews:**
```bash
curl -X GET http://localhost:5000/api/v1/places/PLACE_ID
```

**Get All Users:**
```bash
curl -X GET http://localhost:5000/api/v1/users/
```

**Get Specific User:**
```bash
curl -X GET http://localhost:5000/api/v1/users/USER_ID
```

**Get Reviews for Specific Place:**
```bash
curl -X GET http://localhost:5000/api/v1/reviews/places/PLACE_ID/reviews
```

**Get All Amenities:**
```bash
curl -X GET http://localhost:5000/api/v1/amenities/
```

## Expected Results

### User-Place Relationship (One-to-Many)
- Each place should show its owner information
- Users can own multiple places
- Places belong to exactly one user

### User-Review Relationship (One-to-Many)  
- Users can write multiple reviews
- Each review belongs to exactly one user
- Review responses include user information

### Place-Review Relationship (One-to-Many)
- Places can have multiple reviews
- Each review belongs to exactly one place
- Place responses include review information

### Place-Amenity Relationship (Many-to-Many)
- Places can have multiple amenities
- Amenities can be associated with multiple places
- Association managed through place creation/updates

## Relationship Verification

The responses should demonstrate:

1. **Foreign Key Constraints**: Invalid user_id or place_id in requests return errors
2. **Bidirectional Access**: Can access relationships from both sides
3. **Proper Serialization**: Related objects included in API responses
4. **Authentication**: JWT tokens required for protected endpoints
5. **Authorization**: Admin users can perform restricted operations

## Notes

- Replace `YOUR_ADMIN_TOKEN`, `YOUR_USER_TOKEN`, `USER_ID`, `PLACE_ID`, etc. with actual values from responses
- Some endpoints require admin privileges (amenity management, user management)
- The many-to-many relationship (Place-Amenity) is established during place creation via the amenities list
- All relationships maintain referential integrity through foreign key constraints
