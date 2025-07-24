# HBnB Part 3 - Minimal Version

This is a simplified version of the HBnB application with essential functionality only.

## Features

- User registration and authentication
- JWT-based authorization
- CRUD operations for Users, Places, Amenities, and Reviews
- SQLite database with SQLAlchemy ORM
- RESTful API with Flask-RESTx

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

The API will be available at `http://127.0.0.1:5001`

## API Documentation

Once running, visit `http://127.0.0.1:5001` for interactive API documentation.

## Basic Usage

1. **Register a user**: POST `/api/v1/auth/register`
2. **Login**: POST `/api/v1/auth/login` (returns JWT token)
3. **Use token**: Include `Authorization: Bearer <token>` in headers for protected endpoints

## Endpoints

- **Auth**: `/api/v1/auth/` - Registration and login
- **Users**: `/api/v1/users/` - User management
- **Places**: `/api/v1/places/` - Place management
- **Amenities**: `/api/v1/amenities/` - Amenity management (Admin only)
- **Reviews**: `/api/v1/reviews/` - Review management

## File Structure

```
part3_minimal/
├── run.py              # Application entry point
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── app/
│   ├── __init__.py     # App factory
│   ├── models/         # Database models
│   ├── api/v1/         # API endpoints
│   └── services/       # Business logic (facade)
└── instance/           # Database files
```
