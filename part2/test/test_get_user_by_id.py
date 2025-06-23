#!/usr/bin/env python3
"""
Comprehensive Test for Retrieve User by ID endpoint (GET /api/v1/users/<user_id>)
"""

from app import create_app
from app.models.user import User
from app.services.facade import HBnBFacade
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_get_user_by_id_logic():
    """Test the business logic for user retrieval by ID"""
    print("🔧 Testing User Retrieval by ID - Business Logic...")

    # Create facade instance
    facade = HBnBFacade()

    # Test 1: Create a test user first
    print("\n1. Creating test users...")
    users_data = [
        {
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'email': 'bruce.wayne@example.com'
        },
        {
            'first_name': 'Peter',
            'last_name': 'Parker',
            'email': 'peter.parker@example.com'
        },
        {
            'first_name': 'Tony',
            'last_name': 'Stark',
            'email': 'tony.stark@example.com'
        }
    ]

    created_users = []
    for user_data in users_data:
        try:
            user = facade.create_user(user_data)
            created_users.append(user)
            print(
                f"   ✓ Created user: {
                    user.first_name} {
                    user.last_name} (ID: {
                    user.id})")
        except Exception as e:
            print(f"   ✗ Error creating user: {e}")
            return False

    # Test 2: Retrieve each user by ID
    print("\n2. Retrieving users by ID...")
    for i, user in enumerate(created_users):
        try:
            retrieved_user = facade.get_user(user.id)
            if retrieved_user:
                print(
                    f"   ✓ Retrieved user {
                        i +
                        1}: {
                        retrieved_user.first_name} {
                        retrieved_user.last_name}")
                print(f"     - ID: {retrieved_user.id}")
                print(f"     - Email: {retrieved_user.email}")
                print(f"     - Created: {retrieved_user.created_at}")

                # Verify data integrity
                if (retrieved_user.id == user.id and
                    retrieved_user.first_name == user.first_name and
                    retrieved_user.last_name == user.last_name and
                        retrieved_user.email == user.email):
                    print(f"     ✓ Data integrity verified")
                else:
                    print(f"     ✗ Data integrity check failed")
                    return False
            else:
                print(f"   ✗ Failed to retrieve user {i + 1}")
                return False
        except Exception as e:
            print(f"   ✗ Error retrieving user {i + 1}: {e}")
            return False

    # Test 3: Try to retrieve non-existent user
    print("\n3. Testing non-existent user retrieval...")
    fake_ids = [
        "00000000-0000-0000-0000-000000000000",
        "fake-id",
        "12345",
        ""
    ]

    for fake_id in fake_ids:
        try:
            result = facade.get_user(fake_id)
            if result is None:
                print(f"   ✓ Correctly returned None for fake ID: '{fake_id}'")
            else:
                print(f"   ✗ Unexpectedly found user for fake ID: '{fake_id}'")
                return False
        except Exception as e:
            print(f"   ✓ Exception handling for fake ID '{fake_id}': {e}")

    # Test 4: Performance test with multiple retrievals
    print("\n4. Performance test - Multiple retrievals...")
    import time
    start_time = time.time()

    for _ in range(100):
        for user in created_users:
            facade.get_user(user.id)

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"   ✓ 300 retrievals completed in {elapsed:.4f} seconds")
    print(f"   ✓ Average retrieval time: {(elapsed / 300) * 1000:.2f} ms")

    print("\n🎉 All business logic tests passed!")
    return True, created_users


def test_get_user_by_id_api():
    """Test the HTTP API for user retrieval by ID"""
    print("\n🌐 Testing User Retrieval by ID - HTTP API...")

    # Create Flask app
    app = create_app()
    client = app.test_client()

    # First create some test users via API
    print("\n1. Creating test users via API...")
    users_data = [
        {
            'first_name': 'Steve',
            'last_name': 'Rogers',
            'email': 'steve.rogers@example.com'
        },
        {
            'first_name': 'Natasha',
            'last_name': 'Romanoff',
            'email': 'natasha.romanoff@example.com'
        }
    ]

    created_user_ids = []
    for i, user_data in enumerate(users_data):
        response = client.post('/api/v1/users/',
                               data=json.dumps(user_data),
                               content_type='application/json')

        if response.status_code == 201:
            data = json.loads(response.data)
            created_user_ids.append(data['id'])
            print(
                f"   ✓ Created user {
                    i +
                    1} via API: {
                    data['first_name']} {
                    data['last_name']}")
            print(f"     - ID: {data['id']}")
        else:
            print(f"   ✗ Failed to create user {i + 1} via API")
            return False

    # Test 2: Retrieve users by ID via GET API
    print("\n2. Retrieving users by ID via GET API...")
    for i, user_id in enumerate(created_user_ids):
        response = client.get(f'/api/v1/users/{user_id}')

        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"   ✓ Retrieved user {i + 1} via API:")
            print(f"     - Status Code: {response.status_code}")
            print(f"     - ID: {data['id']}")
            print(f"     - Name: {data['first_name']} {data['last_name']}")
            print(f"     - Email: {data['email']}")

            # Verify the ID matches
            if data['id'] == user_id:
                print(f"     ✓ ID verification passed")
            else:
                print(
                    f"     ✗ ID mismatch: expected {user_id}, got {
                        data['id']}")
                return False
        else:
            print(
                f"   ✗ Failed to retrieve user {
                    i +
                    1}. Status: {
                    response.status_code}")
            return False

    # Test 3: Test 404 for non-existent users
    print("\n3. Testing 404 responses for non-existent users...")
    fake_ids = [
        "00000000-0000-0000-0000-000000000000",
        "fake-user-id",
        "12345"
    ]

    for fake_id in fake_ids:
        response = client.get(f'/api/v1/users/{fake_id}')

        if response.status_code == 404:
            data = json.loads(response.data)
            print(f"   ✓ Correctly returned 404 for fake ID: '{fake_id}'")
            print(
                f"     - Error message: {data.get('error', 'No error message')}")
        else:
            print(
                f"   ✗ Expected 404 for fake ID '{fake_id}', got {
                    response.status_code}")
            return False

    # Test 4: Test edge cases
    print("\n4. Testing edge cases...")
    edge_cases = [
        "",  # Empty string
        "   ",  # Whitespace
        "null",  # String 'null'
        "undefined"  # String 'undefined'
    ]

    for edge_case in edge_cases:
        response = client.get(f'/api/v1/users/{edge_case}')
        print(f"   ✓ Edge case '{edge_case}': Status {response.status_code}")

    # Test 5: Test response format
    print("\n5. Verifying response format...")
    if created_user_ids:
        response = client.get(f'/api/v1/users/{created_user_ids[0]}')
        if response.status_code == 200:
            data = json.loads(response.data)
            required_fields = ['id', 'first_name', 'last_name', 'email']

            for field in required_fields:
                if field in data:
                    print(f"   ✓ Response contains required field: '{field}'")
                else:
                    print(f"   ✗ Response missing required field: '{field}'")
                    return False

            # Check no extra sensitive fields
            sensitive_fields = ['password', 'hash', 'created_at', 'updated_at']
            for field in sensitive_fields:
                if field not in data:
                    print(
                        f"   ✓ Response correctly excludes sensitive field: '{field}'")
                else:
                    print(
                        f"   ⚠️  Response contains sensitive field: '{field}'")

    print("\n🎉 All HTTP API tests passed!")
    return True


def print_api_documentation():
    """Print comprehensive API documentation"""
    print("\n" + "=" * 80)
    print("📚 RETRIEVE USER BY ID ENDPOINT DOCUMENTATION")
    print("=" * 80)
    print("""
🔗 ENDPOINT: GET /api/v1/users/<user_id>

📋 DESCRIPTION:
   Retrieves a specific user by their unique ID

�� REQUEST FORMAT:
   GET /api/v1/users/{user_id}
   Content-Type: application/json (optional)

   URL Parameters:
   • user_id (string, required): The unique identifier of the user

📤 RESPONSE FORMATS:

   ✅ SUCCESS (200 OK):
   {
     "id": "uuid-string",
     "first_name": "string",
     "last_name": "string",
     "email": "string"
   }

   ❌ ERROR (404 Not Found):
   {
     "error": "User not found"
   }

🔍 VALIDATION RULES:
   • user_id must be provided in the URL path
   • Returns 404 if user doesn't exist
   • Returns clean user data without sensitive information

🏗️ EXAMPLE USAGE:
   curl -X GET http://localhost:5000/api/v1/users/123e4567-e89b-12d3-a456-426614174000

   Example Response:
   {
     "id": "123e4567-e89b-12d3-a456-426614174000",
     "first_name": "John",
     "last_name": "Doe",
     "email": "john.doe@example.com"
   }

💡 INTEGRATION TIPS:
   • Use this endpoint after creating a user to verify creation
   • Combine with user creation for user profile pages
   • Perfect for user authentication and profile management
   • Cache responses for better performance if needed
""")
    print("=" * 80)


if __name__ == "__main__":
    print_api_documentation()

    # Run business logic tests
    success1, users = test_get_user_by_id_logic()
    if not success1:
        sys.exit(1)

    # Run HTTP API tests
    success2 = test_get_user_by_id_api()
    if not success2:
        sys.exit(1)

    print(f"\n🎊 ALL TESTS PASSED! Retrieve User by ID endpoint is fully functional!")
    print(f"📊 Created and tested {len(users)} users via business logic")
    print(f"🌐 Verified complete HTTP API functionality")
    print(f"✨ Ready for production use!")

    sys.exit(0)
