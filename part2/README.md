# 🏡 HBnB Evolution Part 2 - API Implementation

Welcome to **HBnB Evolution Part 2**, a fully functional RESTful API implementation for a simplified AirBnB-like platform. This phase implements the complete backend system with a three-layer architecture using Flask-RESTx.

---

## 📌 Project Overview

**HBnB Evolution Part 2** provides a complete REST API for:
- **User Management**: Register, authenticate, and manage user profiles
- **Place Management**: Create, list, and manage rental properties
- **Review System**: Submit and view reviews for places
- **Amenity Management**: Manage property amenities

### 🚀 Key Features
- RESTful API with Flask-RESTx
- Automatic Swagger documentation
- In-memory data persistence
- Comprehensive test suite
- Input validation and error handling
- Three-layer architecture pattern

---

## 🏗️ Architecture Overview

### Three-Layer Architecture

1. **Presentation Layer** (`app/api/v1/`)
   - RESTful API endpoints
   - Request/response handling
   - Input validation
   - Flask-RESTx namespaces

2. **Business Logic Layer** (`app/services/`, `app/models/`)
   - Business rules and logic
   - Data models and entities
   - Facade pattern implementation

3. **Persistence Layer** (`app/persistence/`)
   - Data storage and retrieval
   - Repository pattern
   - In-memory storage implementation

---

## 📂 Project Structure

```
part2/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py      # API blueprint registration
│   │       ├── amenities.py     # Amenity endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       └── user.py          # User endpoints
│   ├── models/
│   │   ├── amenities.py         # Amenity model
│   │   ├── base_models.py       # Base model class
│   │   ├── place.py             # Place model
│   │   ├── reviews.py           # Review model
│   │   └── user.py              # User model
│   ├── persistence/
│   │   └── repository.py        # Repository pattern implementation
│   └── services/
│       ├── __init__.py
│       └── facade.py            # Facade pattern implementation
├── test/
│   ├── test_*.py                # Unit tests
│   └── ...
├── config.py                    # Application configuration
├── run.py                       # Application entry point
├── run_tests.py                 # Test runner with utilities
└── README.md                    # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part2
   ```

2. **Install dependencies**:
   ```bash
   pip install flask flask-restx requests
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

4. **Access the API**:
   - **Swagger UI**: http://127.0.0.1:5001/api/v1/
   - **Base API**: http://127.0.0.1:5001/api/v1/

---

## 🔧 API Endpoints

### Users (`/api/v1/users`)
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user

### Places (`/api/v1/places`)
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/` - Get all places
- `GET /api/v1/places/{id}` - Get place by ID
- `PUT /api/v1/places/{id}` - Update place

### Reviews (`/api/v1/reviews`)
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/` - Get all reviews
- `GET /api/v1/reviews/{id}` - Get review by ID
- `PUT /api/v1/reviews/{id}` - Update review
- `GET /api/v1/places/{place_id}/reviews` - Get reviews for a place

### Amenities (`/api/v1/amenities`)
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/` - Get all amenities
- `GET /api/v1/amenities/{id}` - Get amenity by ID
- `PUT /api/v1/amenities/{id}` - Update amenity

---

## 🧪 Testing

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Categories
```bash
python run_tests.py users        # User endpoint tests
python run_tests.py places       # Place endpoint tests
python run_tests.py reviews      # Review endpoint tests
python run_tests.py amenities    # Amenity endpoint tests
python run_tests.py validation   # Validation tests
```

### Access Swagger Documentation
```bash
python run_tests.py swagger
```

### View Test Examples
```bash
python run_tests.py examples
```

---

## 📋 API Documentation

### Swagger UI
The API automatically generates interactive documentation using Flask-RESTx:
- **URL**: http://127.0.0.1:5001/api/v1/
- **Features**:
  - Interactive API testing
  - Complete endpoint documentation
  - Request/response schemas
  - Model definitions
  - Example requests

### Example API Calls

#### Create a User
```bash
curl -X POST "http://127.0.0.1:5001/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }'
```

#### Create a Place
```bash
curl -X POST "http://127.0.0.1:5001/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A comfortable place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "USER_ID_HERE"
  }'
```

#### Create a Review
```bash
curl -X POST "http://127.0.0.1:5001/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "USER_ID_HERE",
    "place_id": "PLACE_ID_HERE"
  }'
```

---

## 🔍 Key Components

### Models
- **BaseModel**: Common attributes and methods for all entities
- **User**: User management with email validation
- **Place**: Property listings with location and pricing
- **Review**: Rating and commenting system
- **Amenity**: Property features and amenities

### Services
- **HBnBFacade**: Central service layer managing all business logic
- **Repository Pattern**: Abstract data access layer
- **InMemoryRepository**: In-memory data storage implementation

### API Layer
- **Flask-RESTx**: RESTful API framework with automatic documentation
- **Namespaces**: Organized API endpoints by resource type
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Structured error responses

---

## 🧩 Design Patterns

### Facade Pattern
The `HBnBFacade` class provides a simplified interface to the complex subsystem:
- Centralizes business logic
- Manages inter-model relationships
- Provides consistent API for data operations

### Repository Pattern
The `Repository` and `InMemoryRepository` classes abstract data access:
- Separates data access logic from business logic
- Provides consistent interface for data operations
- Enables easy switching between storage backends

### Factory Pattern
The Flask app factory (`create_app()`) enables:
- Configuration-based app creation
- Easy testing with different configurations
- Modular component registration

---

## 🛠️ Development

### Adding New Endpoints
1. Define the model in `app/models/`
2. Add business logic to `app/services/facade.py`
3. Create API endpoints in `app/api/v1/`
4. Register the namespace in `app/api/v1/__init__.py`
5. Write tests in `test/`

### Running in Development Mode
```bash
python run.py
```
The application runs on `http://127.0.0.1:5001` with debug mode enabled.

### Configuration
Edit `config.py` to modify:
- Debug settings
- Secret keys
- Environment-specific configurations

---

## 🚧 Future Enhancements

- **Database Integration**: Replace in-memory storage with persistent database
- **Authentication**: JWT-based user authentication
- **Authorization**: Role-based access control
- **File Upload**: Support for place images
- **Search & Filtering**: Advanced place search capabilities
- **Email Notifications**: User notification system
- **Caching**: Redis-based caching layer

---

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Write comprehensive tests for new features
3. Update documentation for API changes
4. Ensure all tests pass before submitting

---

## 📝 License

This project is part of the Holberton School curriculum.

---

**Happy coding! 🚀**

