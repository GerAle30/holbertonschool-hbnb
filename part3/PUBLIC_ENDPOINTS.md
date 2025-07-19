# Public Endpoints - No Authentication Required

This document lists all API endpoints that are publicly accessible without JWT authentication.

##  Public Endpoints Overview

These endpoints can be accessed without including an `Authorization` header in the request.

### 📍 Places (Read-Only Access)

#### **GET /api/v1/places/**
- **Description**: Retrieve a list of all available places
- **Authentication**: None required
- **Response**: Array of place objects with full details
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/places/"
  ```

#### **GET /api/v1/places/<place_id>**
- **Description**: Retrieve detailed information about a specific place
- **Authentication**: None required
- **Response**: Complete place object with owner, amenities, and reviews
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/places/12345"
  ```

### 👥 Users (Read-Only + Registration)

#### **GET /api/v1/users/**
- **Description**: Retrieve a list of all users
- **Authentication**: None required
- **Response**: Array of user objects (without passwords)
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/users/"
  ```

#### **GET /api/v1/users/<user_id>**
- **Description**: Retrieve user details by ID
- **Authentication**: None required
- **Response**: User object with basic information
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/users/12345"
  ```

#### **POST /api/v1/users/**
- **Description**: Register a new user (account creation)
- **Authentication**: None required
- **Request Body**: User registration data
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
    -H "Content-Type: application/json" \
    -d '{
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "password": "secure_password"
    }'
  ```

### 📝 Reviews (Read-Only Access)

#### **GET /api/v1/reviews/**
- **Description**: Retrieve a list of all reviews
- **Authentication**: None required
- **Response**: Array of review objects
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/reviews/"
  ```

#### **GET /api/v1/reviews/<review_id>**
- **Description**: Retrieve review details by ID
- **Authentication**: None required
- **Response**: Single review object
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/reviews/12345"
  ```

#### **GET /api/v1/reviews/places/<place_id>/reviews**
- **Description**: Get all reviews for a specific place
- **Authentication**: None required
- **Response**: Array of reviews for the specified place
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/reviews/places/12345/reviews"
  ```

### 🏨 Amenities (Full Access)

#### **GET /api/v1/amenities/**
- **Description**: Retrieve a list of all amenities
- **Authentication**: None required
- **Response**: Array of amenity objects
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/amenities/"
  ```

#### **GET /api/v1/amenities/<amenity_id>**
- **Description**: Retrieve amenity details by ID
- **Authentication**: None required
- **Response**: Single amenity object
- **Example**:
  ```bash
  curl -X GET "http://127.0.0.1:5000/api/v1/amenities/12345"
  ```

#### **POST /api/v1/amenities/**
- **Description**: Create a new amenity
- **Authentication**: None required
- **Request Body**: Amenity data
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
    -H "Content-Type: application/json" \
    -d '{"name": "Swimming Pool"}'
  ```

#### **PUT /api/v1/amenities/<amenity_id>**
- **Description**: Update an amenity
- **Authentication**: None required
- **Request Body**: Updated amenity data
- **Example**:
  ```bash
  curl -X PUT "http://127.0.0.1:5000/api/v1/amenities/12345" \
    -H "Content-Type: application/json" \
    -d '{"name": "Olympic Swimming Pool"}'
  ```

###  Authentication

#### **POST /api/v1/auth/login**
- **Description**: User authentication (login)
- **Authentication**: None required (this is how you get a token)
- **Request Body**: Login credentials
- **Response**: JWT access token
- **Example**:
  ```bash
  curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "john@example.com",
      "password": "secure_password"
    }'
  ```

## 🔒 What's NOT Public

The following endpoints **require JWT authentication**:

### Protected Endpoints
- **POST /api/v1/places/** - Create place
- **PUT /api/v1/places/<place_id>** - Update place
- **POST /api/v1/reviews/** - Create review
- **PUT /api/v1/reviews/<review_id>** - Update review
- **DELETE /api/v1/reviews/<review_id>** - Delete review
- **PUT /api/v1/users/<user_id>** - Update user profile
- **GET /api/v1/auth/protected** - Test protected endpoint

## 📊 Response Format

All public endpoints return JSON responses with appropriate HTTP status codes:

### Success Responses
- **200 OK**: Successful GET requests
- **201 Created**: Successful POST requests (creation)

### Error Responses
- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## 🧪 Testing Public Endpoints

You can test these endpoints without any authentication headers:

```bash
# Test the two specifically mentioned public endpoints
curl -X GET "http://127.0.0.1:5000/api/v1/places/"
curl -X GET "http://127.0.0.1:5000/api/v1/places/some-place-id"

# Test other public endpoints
curl -X GET "http://127.0.0.1:5000/api/v1/users/"
curl -X GET "http://127.0.0.1:5000/api/v1/reviews/"
curl -X GET "http://127.0.0.1:5000/api/v1/amenities/"
```

##  Key Points

1. **No Authentication Required**: These endpoints work without JWT tokens
2. **Read-Only Access**: Most public endpoints are for data retrieval
3. **Registration Available**: New users can register publicly
4. **Full Amenity Access**: Amenities can be created/updated publicly
5. **Place Details**: Complete place information is publicly available
6. **Review Visibility**: All reviews are publicly readable

This design allows for public browsing of places and reviews while protecting sensitive operations behind authentication.
