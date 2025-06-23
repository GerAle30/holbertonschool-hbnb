#!/usr/bin/env python3
"""
HTTP API Test script for Create User endpoint (POST /api/v1/users/)
This test demonstrates the full Flask REST API functionality
"""

from flask import Flask
from app.api.v1 import blueprint
from app import create_app
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_api_create_user():
    """Test the Create User API endpoint via HTTP requests"""
    print("Testing Create User API (POST /api/v1/users/) via HTTP...")

    # Create Flask app and register blueprint
    app = Flask(__name__)
    app.register_blueprint(blueprint)

    # Create test client
    client = app.test_client()

    # Test 1: Create a valid user
    print("\n1. Testing valid user creation...")
    user_data = {
        'first_name': 'Diana',
        'last_name': 'Prince',
        'email': 'diana.prince@example.com'
    }

    response = client.post('/api/v1/users/',
                           data=json.dumps(user_data),
                           content_type='application/json')

    if response.status_code == 201:
        data = json.loads(response.data)
        print(f"   ✓ User created successfully!")
        print(f"   - Status Code: {response.status_code}")
        print(f"   - ID: {data['id']}")
        print(f"   - Name: {data['first_name']} {data['last_name']}")
        print(f"   - Email: {data['email']}")
        created_user_id = data['id']
    else:
        print(f"   ✗ Failed to create user. Status: {response.status_code}")
        print(f"   Response: {response.data}")
        return False

    # Test 2: Try to create duplicate email user
    print("\n2. Testing duplicate email handling...")
    duplicate_data = {
        'first_name': 'Diana',
        'last_name': 'Clone',
        'email': 'diana.prince@example.com'  # Same email
    }

    response = client.post('/api/v1/users/',
                           data=json.dumps(duplicate_data),
                           content_type='application/json')

    if response.status_code == 400:
        data = json.loads(response.data)
        print(f"   ✓ Correctly rejected duplicate email!")
        print(f"   - Status Code: {response.status_code}")
        print(f"   - Error: {data.get('error', 'Unknown error')}")
    else:
        print(
            f"   ✗ Should have returned 400 for duplicate email. Got: {
                response.status_code}")
        return False

    # Test 3: Test invalid data (missing required field)
    print("\n3. Testing invalid data handling...")
    invalid_data = {
        'first_name': 'Bruce',
        # Missing last_name and email
    }

    response = client.post('/api/v1/users/',
                           data=json.dumps(invalid_data),
                           content_type='application/json')

    if response.status_code == 400:
        print(f"   ✓ Correctly rejected invalid data!")
        print(f"   - Status Code: {response.status_code}")
    else:
        print(
            f"   ✗ Should have returned 400 for invalid data. Got: {
                response.status_code}")
        return False

    # Test 4: Verify created user can be retrieved
    print("\n4. Verifying created user can be retrieved...")
    response = client.get(f'/api/v1/users/{created_user_id}')

    if response.status_code == 200:
        data = json.loads(response.data)
        print(f"   ✓ User retrieved successfully!")
        print(f"   - ID: {data['id']}")
        print(f"   - Name: {data['first_name']} {data['last_name']}")
        print(f"   - Email: {data['email']}")
    else:
        print(
            f"   ✗ Failed to retrieve created user. Status: {
                response.status_code}")
        return False

    # Test 5: Test retrieving all users
    print("\n5. Testing user list endpoint...")
    response = client.get('/api/v1/users/')

    if response.status_code == 200:
        data = json.loads(response.data)
        print(f"   ✓ Retrieved user list successfully!")
        print(f"   - Status Code: {response.status_code}")
        print(f"   - Number of users: {len(data)}")
        for user in data:
            print(
                f"     - {user['first_name']} {user['last_name']} ({user['email']})")
    else:
        print(
            f"   ✗ Failed to retrieve user list. Status: {
                response.status_code}")
        return False

    # Test 6: Create another user to test multiple users
    print("\n6. Creating another user...")
    user_data_2 = {
        'first_name': 'Clark',
        'last_name': 'Kent',
        'email': 'clark.kent@example.com'
    }

    response = client.post('/api/v1/users/',
                           data=json.dumps(user_data_2),
                           content_type='application/json')

    if response.status_code == 201:
        data = json.loads(response.data)
        print(f"   ✓ Second user created successfully!")
        print(f"   - ID: {data['id']}")
        print(f"   - Name: {data['first_name']} {data['last_name']}")
        print(f"   - Email: {data['email']}")
    else:
        print(
            f"   ✗ Failed to create second user. Status: {
                response.status_code}")
        return False

    print("\n🎉 All API tests passed! Create User endpoint is fully functional via HTTP!")
    return True


def print_api_documentation():
    """Print API documentation for the Create User endpoint"""
    print("\n" + "=" * 80)
    print(" CREATE USER ENDPOINT DOCUMENTATION")
    print("=" * 80)
    print("""
 ENDPOINT: POST /api/v1/users/

 DESCRIPTION:
   Creates a new user in the system with validation

 REQUEST FORMAT:
   Content-Type: application/json

   {
     "first_name": "string (required, max 50 chars)",
     "last_name": "string (required, max 50 chars)",
     "email": "string (required, valid email format)"
   }

 RESPONSE FORMATS:

    SUCCESS (201 Created):
   {
     "id": "uuid-string",
     "first_name": "string",
     "last_name": "string",
     "email": "string"
   }

    ERROR (400 Bad Request):
   {
     "error": "Email already registered"
   }

    ERROR (400 Bad Request):
   {
     "error": "Invalid input data"
   }

 VALIDATION RULES:
   • first_name: Required, non-empty, max 50 characters
   • last_name: Required, non-empty, max 50 characters
   • email: Required, valid email format, must be unique

 EXAMPLE USAGE:
   curl -X POST http://localhost:5000/api/v1/users/ \\
        -H "Content-Type: application/json" \\
        -d '{
          "first_name": "John",
          "last_name": "Doe",
          "email": "john.doe@example.com"
        }'
""")
    print("=" * 80)


if __name__ == "__main__":
    print_api_documentation()
    success = test_api_create_user()
    sys.exit(0 if success else 1)
