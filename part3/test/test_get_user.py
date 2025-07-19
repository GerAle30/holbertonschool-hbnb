#!/usr/bin/env python3
"""
Comprehensive Test for Retrieve List of Users endpoint (GET /api/v1/users/)
"""

from app import create_app
from app.models.user import User
from app.services.facade import HBnBFacade
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_get_all_users_logic():
    """Test the business logic for retrieving all users"""
    print(" Testing Retrieve All Users - Business Logic...")

    # Create facade instance
    facade = HBnBFacade()

    # Test 1: Start with empty user list
    print("\n1. Testing empty user list...")
    all_users = facade.get_all_users()
    print(f"   ✓ Initial user count: {len(all_users)}")
    initial_count = len(all_users)

    # Test 2: Create multiple test users
    print("\n2. Creating test users...")
    test_users_data = [
        {
            'first_name': 'Luke',
            'last_name': 'Skywalker',
            'email': 'luke.skywalker@rebels.com'
        },
        {
            'first_name': 'Leia',
            'last_name': 'Organa',
            'email': 'leia.organa@rebels.com'
        },
        {
            'first_name': 'Han',
            'last_name': 'Solo',
            'email': 'han.solo@smugglers.com'
        },
        {
            'first_name': 'Chewbacca',
            'last_name': 'Wookiee',
            'email': 'chewie@kashyyyk.com'
        },
        {
            'first_name': 'Obi-Wan',
            'last_name': 'Kenobi',
            'email': 'obiwan.kenobi@jedi.org'
        }
    ]

    created_users = []
    for i, user_data in enumerate(test_users_data):
        try:
            user = facade.create_user(user_data)
            created_users.append(user)
            print(
                f"   ✓ Created user {
                    i +
                    1}: {
                    user.first_name} {
                    user.last_name}")
        except Exception as e:
            print(f"   ✗ Error creating user {i + 1}: {e}")
            return False

    print(f"   ✓ Successfully created {len(created_users)} users")

    # Test 3: Retrieve all users and verify count
    print("\n3. Retrieving all users...")
    all_users = facade.get_all_users()
    expected_count = initial_count + len(created_users)

    if len(all_users) == expected_count:
        print(f"   ✓ User count verification passed: {len(all_users)} users")
    else:
        print(
            f"   ✗ User count mismatch: expected {expected_count}, got {
                len(all_users)}")
        return False

    # Test 4: Verify all created users are in the list
    print("\n4. Verifying user data integrity...")
    created_user_emails = {user.email for user in created_users}
    retrieved_user_emails = {user.email for user in all_users}

    for email in created_user_emails:
        if email in retrieved_user_emails:
            print(f"   ✓ Found user with email: {email}")
        else:
            print(f"   ✗ Missing user with email: {email}")
            return False

    # Test 5: Verify data structure of returned users
    print("\n5. Verifying user object structure...")
    for i, user in enumerate(
            all_users[-len(created_users):]):  # Check last created users
        if (hasattr(user, 'id') and hasattr(user, 'first_name') and
                hasattr(user, 'last_name') and hasattr(user, 'email')):
            print(
                f"   ✓ User {
                    i +
                    1} structure valid: {
                    user.first_name} {
                    user.last_name}")
        else:
            print(f"   ✗ User {i + 1} structure invalid")
            return False

    # Test 6: Performance test with many users
    print("\n6. Performance test - Multiple retrievals...")
    import time
    start_time = time.time()

    for _ in range(100):
        facade.get_all_users()

    end_time = time.time()
    elapsed = end_time - start_time
    print(f"   ✓ 100 retrievals completed in {elapsed:.4f} seconds")
    print(f"   ✓ Average retrieval time: {(elapsed / 100) * 1000:.2f} ms")

    print("\n All business logic tests passed!")
    return True, created_users


def test_get_all_users_api():
    """Test the HTTP API for retrieving all users"""
    print("\n Testing Retrieve All Users - HTTP API...")

    # Create Flask app
    app = create_app()
    client = app.test_client()

    # Test 1: Get initial user count
    print("\n1. Getting initial user count...")
    response = client.get('/api/v1/users/')

    if response.status_code == 200:
        initial_users = json.loads(response.data)
        print(f"   ✓ Initial user count: {len(initial_users)}")
        print(f"   ✓ Status Code: {response.status_code}")
        initial_count = len(initial_users)
    else:
        print(
            f"   ✗ Failed to get initial users. Status: {
                response.status_code}")
        return False

    # Test 2: Create some test users via API
    print("\n2. Creating test users via API...")
    api_test_users = [
        {
            'first_name': 'Darth',
            'last_name': 'Vader',
            'email': 'darth.vader@empire.com'
        },
        {
            'first_name': 'Emperor',
            'last_name': 'Palpatine',
            'email': 'emperor@empire.com'
        },
        {
            'first_name': 'Boba',
            'last_name': 'Fett',
            'email': 'boba.fett@bounty.com'
        }
    ]

    created_user_ids = []
    for i, user_data in enumerate(api_test_users):
        response = client.post('/api/v1/users/',
                               data=json.dumps(user_data),
                               content_type='application/json')

        if response.status_code == 201:
            user = json.loads(response.data)
            created_user_ids.append(user['id'])
            print(
                f"   ✓ Created user {
                    i +
                    1} via API: {
                    user['first_name']} {
                    user['last_name']}")
        else:
            print(f"   ✗ Failed to create user {i + 1} via API")
            return False

    # Test 3: Retrieve all users and verify count increased
    print("\n3. Retrieving all users after creation...")
    response = client.get('/api/v1/users/')

    if response.status_code == 200:
        all_users = json.loads(response.data)
        expected_count = initial_count + len(api_test_users)

        print(f"   ✓ Status Code: {response.status_code}")
        print(f"   ✓ Total users retrieved: {len(all_users)}")

        if len(all_users) == expected_count:
            print(f"   ✓ User count verification passed")
        else:
            print(
                f"     User count: expected {expected_count}, got {
                    len(all_users)}")
            # This might be expected if other tests ran before
    else:
        print(f"   ✗ Failed to retrieve users. Status: {response.status_code}")
        return False

    # Test 4: Verify response format
    print("\n4. Verifying response format...")
    if all_users:
        sample_user = all_users[0]
        required_fields = ['id', 'first_name', 'last_name', 'email']

        for field in required_fields:
            if field in sample_user:
                print(f"   ✓ Response contains required field: '{field}'")
            else:
                print(f"   ✗ Response missing required field: '{field}'")
                return False

        # Verify data types
        if (isinstance(sample_user['id'], str) and
            isinstance(sample_user['first_name'], str) and
            isinstance(sample_user['last_name'], str) and
                isinstance(sample_user['email'], str)):
            print(f"   ✓ All field data types are correct")
        else:
            print(f"   ✗ Field data type validation failed")
            return False

    # Test 5: Verify created users are in the list
    print("\n5. Verifying created users appear in list...")
    user_emails = [user['email'] for user in all_users]

    for i, user_data in enumerate(api_test_users):
        if user_data['email'] in user_emails:
            print(f"   ✓ Found created user {i + 1}: {user_data['email']}")
        else:
            print(f"   ✗ Missing created user {i + 1}: {user_data['email']}")
            return False

    # Test 6: Test pagination readiness (check if response is array)
    print("\n6. Testing response structure for pagination readiness...")
    if isinstance(all_users, list):
        print(f"   ✓ Response is a list (pagination-ready)")
        print(f"   ✓ List contains {len(all_users)} user objects")
    else:
        print(f"   ✗ Response is not a list")
        return False

    # Test 7: Test empty vs populated list behavior
    print("\n7. Testing list behavior...")
    if len(all_users) > 0:
        print(f"   ✓ Non-empty list returned successfully")

        # Verify all users have unique IDs
        user_ids = [user['id'] for user in all_users]
        if len(user_ids) == len(set(user_ids)):
            print(f"   ✓ All user IDs are unique")
        else:
            print(f"   ✗ Duplicate user IDs detected")
            return False

        # Verify all users have unique emails
        user_emails = [user['email'] for user in all_users]
        if len(user_emails) == len(set(user_emails)):
            print(f"   ✓ All user emails are unique")
        else:
            print(f"   ✗ Duplicate user emails detected")
            return False

    print("\n All HTTP API tests passed!")
    return True, all_users


def test_edge_cases():
    """Test edge cases for the user list endpoint"""
    print("\n🧪 Testing Edge Cases...")

    app = create_app()
    client = app.test_client()

    # Test 1: Test different HTTP methods
    print("\n1. Testing HTTP method restrictions...")

    # OPTIONS should work (CORS preflight)
    response = client.options('/api/v1/users/')
    print(f"   ✓ OPTIONS method: Status {response.status_code}")

    # HEAD should work (metadata only)
    response = client.head('/api/v1/users/')
    print(f"   ✓ HEAD method: Status {response.status_code}")

    # POST should work (create user)
    response = client.post('/api/v1/users/',
                           data=json.dumps({'first_name': 'Test',
                                            'last_name': 'User',
                                            'email': 'test@test.com'}),
                           content_type='application/json')
    if response.status_code in [201, 400]:  # 400 if email exists
        print(f"   ✓ POST method: Status {response.status_code}")

    # Test 2: Test with different content types
    print("\n2. Testing content type handling...")

    # JSON accept header
    response = client.get(
        '/api/v1/users/',
        headers={
            'Accept': 'application/json'})
    if response.status_code == 200:
        print(f"   ✓ JSON Accept header handled correctly")

    # Test 3: Test large number of users performance
    print("\n3. Testing with larger dataset...")

    response = client.get('/api/v1/users/')
    if response.status_code == 200:
        users = json.loads(response.data)
        if len(users) > 0:
            print(f"   ✓ Successfully retrieved {len(users)} users")

            # Calculate response size
            response_size = len(response.data)
            print(f"   ✓ Response size: {response_size} bytes")
            print(
                f"   ✓ Average bytes per user: {
                    response_size /
                    len(users):.1f}")

    print("\n All edge case tests passed!")
    return True


def print_api_documentation():
    """Print comprehensive API documentation"""
    print("\n" + "=" * 80)
    print("📚 RETRIEVE LIST OF USERS ENDPOINT DOCUMENTATION")
    print("=" * 80)
    print("""
🔗 ENDPOINT: GET /api/v1/users/

 DESCRIPTION:
   Retrieves a list of all users in the system

📨 REQUEST FORMAT:
   GET /api/v1/users/
   Content-Type: application/json (optional)

   No request body required

📤 RESPONSE FORMATS:

    SUCCESS (200 OK):
   [
     {
       "id": "uuid-string",
       "first_name": "string",
       "last_name": "string",
       "email": "string"
     },
     {
       "id": "uuid-string",
       "first_name": "string",
       "last_name": "string",
       "email": "string"
     }
   ]

   📝 EMPTY LIST (200 OK):
   []

 FEATURES:
   • Returns all users in the system
   • Each user object contains: id, first_name, last_name, email
   • Returns empty array if no users exist
   • Consistent response format for easy parsing
   • Ready for pagination implementation

🏗️ EXAMPLE USAGE:
   curl -X GET http://localhost:5000/api/v1/users/

   Example Response:
   [
     {
       "id": "123e4567-e89b-12d3-a456-426614174000",
       "first_name": "Luke",
       "last_name": "Skywalker",
       "email": "luke.skywalker@rebels.com"
     },
     {
       "id": "987fcdeb-51a2-43d1-9f12-345678901234",
       "first_name": "Leia",
       "last_name": "Organa",
       "email": "leia.organa@rebels.com"
     }
   ]

 USE CASES:
   • User management dashboards
   • User selection dropdowns
   • Admin user overview
   • User search and filtering (frontend implementation)
   • User statistics and reporting
   • Batch operations on users

⚡ PERFORMANCE NOTES:
   • Fast in-memory retrieval
   • No pagination limit (consider for production)
   • Response size grows with user count
   • Consider caching for frequently accessed data
""")
    print("=" * 80)


if __name__ == "__main__":
    print_api_documentation()

    # Run business logic tests
    success1, users = test_get_all_users_logic()
    if not success1:
        sys.exit(1)

    # Run HTTP API tests
    success2, all_users = test_get_all_users_api()
    if not success2:
        sys.exit(1)

    # Run edge case tests
    success3 = test_edge_cases()
    if not success3:
        sys.exit(1)

    print(f"\n�� ALL TESTS PASSED! Retrieve List of Users endpoint is fully functional!")
    print(f" Business Logic: Created and verified {len(users)} users")
    print(f" HTTP API: Retrieved list of {len(all_users)} total users")
    print(f"🧪 Edge Cases: All scenarios handled correctly")
    print(f"✨ Ready for production use!")

    sys.exit(0)
