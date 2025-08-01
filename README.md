# 🏡 HBnB Evolution - Complete AirBnB Clone

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Welcome to **HBnB Evolution**, a comprehensive simplified clone of AirBnB featuring user management, property listings, reviews, and authentication systems. This project demonstrates modern web development practices with a three-layer architecture using Flask-RESTx.

---

## 📌 Project Overview

**HBnB Evolution** is a full-stack web application that allows users to:

- 🔐 **User Authentication** - Register, login, and secure sessions with JWT
- 🏠 **Property Management** - Create, list, and manage rental properties
- ⭐ **Review System** - Submit and view reviews for places
- 🏨 **Amenity Management** - Manage property amenities and features
- 🔒 **Security Features** - Role-based access control and data validation

---

## 🚀 Key Features

### Core Functionality
- **RESTful API** with Flask-RESTx
- **Automatic Swagger Documentation**
- **JWT-based Authentication**
- **Role-based Authorization**
- **Comprehensive Input Validation**
- **Three-layer Architecture Pattern**

### Security Features
- **Password Hashing** with bcrypt
- **JWT Token Management**
- **Owner-only Operations** (users can only modify their own data)
- **Admin Privileges** for system management
- **Input Sanitization** and validation

### Developer Features
- **Interactive API Documentation** (Swagger UI)
- **Comprehensive Test Suite**
- **Error Handling** with proper HTTP status codes
- **Logging** and debugging capabilities

---

## 🏗️ Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Users     │ │   Places    │ │   Reviews   │           │
│  │  /api/v1/   │ │  /api/v1/   │ │  /api/v1/   │           │
│  │   users     │ │   places    │ │   reviews   │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 BUSINESS LOGIC LAYER                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 HBnB Facade                             │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │ │
│  │  │    User     │ │    Place    │ │   Review    │       │ │
│  │  │   Models    │ │   Models    │ │   Models    │       │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 PERSISTENCE LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              Repository Pattern                          │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐       │ │
│  │  │ InMemory    │ │ InMemory    │ │ InMemory    │       │ │
│  │  │Repository   │ │Repository   │ │Repository   │       │ │
│  │  └─────────────┘ └─────────────┘ └─────────────┘       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
holbertonschool-hbnb/
├── part1/                          # 📋 Technical Documentation
│   ├── README.md                   # Architecture diagrams & specifications
│   ├── *.png                       # UML diagrams and mockups
│   └── diagrams/                   # Mermaid.js diagrams
├── part2/                          # 🔧 Basic API Implementation
│   ├── app/
│   │   ├── __init__.py             # Flask app factory
│   │   ├── api/v1/                 # API endpoints
│   │   ├── models/                 # Data models
│   │   ├── persistence/            # Data storage
│   │   └── services/               # Business logic
│   ├── test/                       # Unit tests
│   ├── run.py                      # Application entry point
│   └── README.md                   # Basic API documentation
├── part3/                          # 🔐 Authentication & Authorization
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── auth.py            # JWT authentication
│   │   │   ├── users.py           # User management
│   │   │   ├── places.py          # Place management
│   │   │   ├── reviews.py         # Review management
│   │   │   └── amenities.py       # Amenity management
│   │   ├── models/                # Enhanced models
│   │   ├── persistence/           # Database repositories
│   │   ├── services/              # Business logic with auth
│   │   └── utils/                 # RBAC utilities
│   ├── instance/                  # SQLite database
│   ├── requirements.txt           # Python dependencies
│   ├── run.py                     # Application entry point
│   └── README.md                  # Authentication documentation
├── part4/                          # 🌐 Frontend Implementation
│   ├── index.html                 # Main page with place listings
│   ├── login.html                 # User authentication page
│   ├── place.html                 # Detailed place view
│   ├── add_review.html           # Review submission form
│   ├── scripts.js                 # Frontend JavaScript logic
│   ├── css/
│   │   └── styles.css            # Complete styling
│   ├── images/                    # Place images and icons
│   │   ├── logo.png
│   │   ├── *.png                 # Place thumbnails
│   │   └── icons/                # UI icons
│   └── README.md                  # Frontend documentation
└── README.md                      # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.7+**
- **pip** (Python package manager)
- **Git** (for version control)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb
   ```

2. **Navigate to the latest version (Part 3):**
   ```bash
   cd part3
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Access the API:**
   - **Swagger UI**: [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)
   - **Base API**: [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)

### 🌐 Full-Stack Experience (Frontend + Backend)

For the complete user experience with the web interface:

1. **Start the backend** (follow steps above)

2. **Navigate to the frontend:**
   ```bash
   cd ../part4
   ```

3. **Serve the frontend:**
   ```bash
   # Using Python's built-in server
   python3 -m http.server 8000
   
   # Or using Node.js http-server
   npx http-server
   ```

4. **Access the web application:**
   - **Frontend UI**: [http://localhost:8000](http://localhost:8000)
   - **Login Page**: [http://localhost:8000/login.html](http://localhost:8000/login.html)

5. **Experience the full application:**
   - Browse available places
   - Create an account or login
   - View detailed place information
   - Add reviews to places
   - Manage your listings

---

## 🔧 API Documentation

### 📍 Public Endpoints (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/places/` | List all places |
| `GET` | `/api/v1/places/{id}` | Get place details |
| `GET` | `/api/v1/users/` | List all users |
| `GET` | `/api/v1/users/{id}` | Get user details |
| `POST` | `/api/v1/users/` | Register new user |
| `GET` | `/api/v1/reviews/` | List all reviews |
| `GET` | `/api/v1/amenities/` | List all amenities |
| `POST` | `/api/v1/auth/login` | User login |

### 🔒 Protected Endpoints (Authentication Required)

| Method | Endpoint | Description | Authorization |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/places/` | Create place | Owner only |
| `PUT` | `/api/v1/places/{id}` | Update place | Owner/Admin only |
| `POST` | `/api/v1/reviews/` | Create review | Authenticated users |
| `PUT` | `/api/v1/reviews/{id}` | Update review | Owner/Admin only |
| `DELETE` | `/api/v1/reviews/{id}` | Delete review | Owner/Admin only |
| `PUT` | `/api/v1/users/{id}` | Update user | Owner/Admin only |

### 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication:

1. **Register** a new user: `POST /api/v1/users/`
2. **Login** to get a token: `POST /api/v1/auth/login`
3. **Use the token** in subsequent requests:
   ```bash
   curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
        -X POST http://127.0.0.1:5000/api/v1/places/
   ```

---

## 📝 Example Usage

### 1. Register a New User
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

### 2. Login and Get Token
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "secure_password"
  }'
```

### 3. Create a Place (with token)
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A beautiful place to stay",
    "price": 100.0,
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

### 4. Create a Review
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "USER_ID",
    "place_id": "PLACE_ID"
  }'
```

---

## 🧪 Testing

### Run All Tests
```bash
cd part3
python run_tests.py
```

### Run Specific Test Categories
```bash
python run_tests.py auth          # Authentication tests
python run_tests.py users         # User endpoint tests
python run_tests.py places        # Place endpoint tests
python run_tests.py reviews       # Review endpoint tests
python run_tests.py amenities     # Amenity endpoint tests
```

### Custom Test Scripts
```bash
# Test review validation logic
python test_review_validation.py

# Test authentication flows
python test_auth.py

# Test password hashing
python test_password_hashing.py
```

---

## 🔒 Security Features

### Authentication & Authorization
- **JWT-based authentication** with secure token generation
- **Password hashing** using bcrypt
- **Role-based access control** (users vs admins)
- **Owner-only operations** (users can only modify their own data)

### Input Validation
- **Comprehensive data validation** for all endpoints
- **SQL injection prevention**
- **XSS protection**
- **Rate limiting** capabilities

### Security Rules
- Users can only review places they don't own
- Users can only review each place once
- Only owners can update their places and reviews
- Admin users have elevated privileges

---

## 🛠️ Development

### Adding New Features

1. **Define the model** in `app/models/`
2. **Add business logic** to `app/services/facade.py`
3. **Create API endpoints** in `app/api/v1/`
4. **Register the namespace** in `app/api/v1/__init__.py`
5. **Write comprehensive tests** in `test/`

### Environment Configuration

Edit `config.py` to modify:
- Debug settings
- Secret keys
- JWT configuration
- Database settings

### Running in Development Mode
```bash
# With debug mode enabled
python run.py

# The application runs on http://127.0.0.1:5000
```

---

## 📊 Project Evolution

| Phase | Description | Status |
|-------|-------------|--------|
| **Part 1** | Technical Documentation & UML Diagrams | ✅ Complete |
| **Part 2** | Basic API Implementation | ✅ Complete |
| **Part 3** | Authentication & Authorization + Database | ✅ Complete |
| **Part 4** | Frontend Implementation | ✅ Complete |
| **Part 5** | Advanced Features & Deployment | 🔄 Future |

---

## 🔮 Future Enhancements

- **Database Integration** - PostgreSQL/MySQL support
- **File Upload** - Support for place images
- **Real-time Features** - WebSocket notifications
- **Advanced Search** - Elasticsearch integration
- **Caching** - Redis-based caching layer
- **Email Notifications** - User notification system
- **Mobile API** - Mobile-optimized endpoints
- **Payment Integration** - Stripe/PayPal support

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Follow the existing code structure and patterns**
4. **Write comprehensive tests** for new features
5. **Update documentation** for API changes
6. **Ensure all tests pass**: `python run_tests.py`
7. **Submit a pull request**

### Code Style
- Follow **PEP 8** Python style guide
- Use **meaningful variable names**
- Include **docstrings** for all functions
- Write **comprehensive tests**

---

## 📋 API Reference

For detailed API documentation, see:
- **Part 2**: [Basic API Documentation](part2/README.md)
- **Part 3**: [Authentication Documentation](part3/README.md)
- **Public Endpoints**: [Public API Guide](part3/PUBLIC_ENDPOINTS.md)
- **Protected Endpoints**: [Secured API Guide](part3/SECURED_ENDPOINTS.md)

---

## 📄 License

This project is part of the **Holberton School curriculum** and is licensed under the MIT License.

---

## 👥 Authors

- **Alejandro** - *Implementation & Documentation*
- **Holberton School** - *Project Requirements & Guidance*

---

## 🔗 Links

- **GitHub Repository**: [holbertonschool-hbnb](https://github.com/GerAle30/holbertonschool-hbnb)
- **Swagger Documentation**: [http://127.0.0.1:5000/api/v1/](http://127.0.0.1:5000/api/v1/)
- **Project Documentation**: [Technical Docs](part1/README.md)

---

## 📞 Support

If you encounter any issues or have questions:

1. **Check the documentation** in each part's README
2. **Review the test files** for usage examples
3. **Check the Swagger UI** for API specifications
4. **Create an issue** in the GitHub repository

---

**Happy coding! 🚀**

*Built with ❤️ for the Holberton School community*
