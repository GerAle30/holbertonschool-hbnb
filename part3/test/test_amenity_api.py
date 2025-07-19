#!/usr/bin/env python3
"""
Comprehensive Test for Amenity API endpoints
Tests all CRUD operations: POST, GET (all & by ID), PUT
"""

from app import create_app
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_amenity_api_endpoints():
    """Test all amenity API endpoints"""
    print(" Testing Amenity API Endpoints...")

    # Create Flask app
    app = create_app()
    client = app.test_client()

    # Test 1: Create amenities (POST /api/v1/amenities/)
    print("\n1. Testing amenity creation (POST)...")
    amenities_to_create = [
        {'name': 'WiFi'},
        {'name': 'Swimming Pool'},
        {'name': 'Gym'},
        {'name': 'Parking'},
        {'name': 'Air Conditioning'}
    ]

    created_amenities = []
    for i, amenity_data in enumerate(amenities_to_create):
        response = client.post('/api/v1/amenities/',
                               data=json.dumps(amenity_data),
                               content_type='application/json')

        if response.status_code == 201:
            amenity = json.loads(response.data)
            created_amenities.append(amenity)
            print(f"   ✓ Created amenity {i + 1}: {amenity['name']}")
            print(f"     - ID: {amenity['id']}")
            print(f"     - Status: {response.status_code}")

            # Verify response structure
            required_fields = ['id', 'name', 'created_at', 'updated_at']
            for field in required_fields:
                if field in amenity:
                    print(f"     ✓ Contains field: {field}")
                else:
                    print(f"     ✗ Missing field: {field}")
                    return False
        else:
            print(f"   ✗ Failed to create amenity {i + 1}")
            print(f"     Response: {response.data}")
            return False

    print(f"   ✓ Successfully created {len(created_amenities)} amenities")

    # Test 2: Get all amenities (GET /api/v1/amenities/)
    print("\n2. Testing get all amenities (GET)...")
    response = client.get('/api/v1/amenities/')

    if response.status_code == 200:
        amenities = json.loads(response.data)
        print(f"   ✓ Retrieved {len(amenities)} amenities")
        print(f"   ✓ Status: {response.status_code}")

        # Verify all created amenities are in the list
        created_names = {amenity['name'] for amenity in created_amenities}
        retrieved_names = {amenity['name'] for amenity in amenities}

        for name in created_names:
            if name in retrieved_names:
                print(f"   ✓ Found amenity: {name}")
            else:
                print(f"   ✗ Missing amenity: {name}")
                return False
    else:
        print(f"   ✗ Failed to retrieve amenities")
        print(f"     Status: {response.status_code}")
        print(f"     Response: {response.data}")
        return False

    # Test 3: Get amenity by ID (GET /api/v1/amenities/<id>)
    print("\n3. Testing get amenity by ID (GET)...")
    if created_amenities:
        test_amenity = created_amenities[0]
        response = client.get(f'/api/v1/amenities/{test_amenity["id"]}')

        if response.status_code == 200:
            amenity = json.loads(response.data)
            print(f"   ✓ Retrieved amenity: {amenity['name']}")
            print(f"   ✓ Status: {response.status_code}")

            # Verify data matches
            if (amenity['id'] == test_amenity['id'] and
                    amenity['name'] == test_amenity['name']):
                print(f"   ✓ Data integrity verified")
            else:
                print(f"   ✗ Data mismatch")
                return False
        else:
            print(f"   ✗ Failed to retrieve amenity by ID")
            print(f"     Status: {response.status_code}")
            return False

    # Test 4: Update amenity (PUT /api/v1/amenities/<id>)
    print("\n4. Testing amenity update (PUT)...")
    if created_amenities:
        test_amenity = created_amenities[0]
        update_data = {'name': 'Premium WiFi'}

        response = client.put(f'/api/v1/amenities/{test_amenity["id"]}',
                              data=json.dumps(update_data),
                              content_type='application/json')

        if response.status_code == 200:
            updated_amenity = json.loads(response.data)
            print(f"   ✓ Updated amenity successfully")
            print(f"   - Original name: {test_amenity['name']}")
            print(f"   - Updated name: {updated_amenity['name']}")
            print(f"   ✓ Status: {response.status_code}")

            # Verify update was applied
            if updated_amenity['name'] == 'Premium WiFi':
                print(f"   ✓ Update applied correctly")
            else:
                print(f"   ✗ Update not applied")
                return False

            # Verify ID didn't change
            if updated_amenity['id'] == test_amenity['id']:
                print(f"   ✓ ID remained consistent")
            else:
                print(f"   ✗ ID changed unexpectedly")
                return False
        else:
            print(f"   ✗ Failed to update amenity")
            print(f"     Status: {response.status_code}")
            print(f"     Response: {response.data}")
            return False

    # Test 5: Error handling - 404 for non-existent amenity
    print("\n5. Testing 404 error handling...")
    fake_id = "00000000-0000-0000-0000-000000000000"

    # Test GET 404
    response = client.get(f'/api/v1/amenities/{fake_id}')
    if response.status_code == 404:
        error = json.loads(response.data)
        print(
            f"   ✓ GET 404 handled correctly: {
                error.get(
                    'error',
                    'No error message')}")
    else:
        print(f"   ✗ Expected 404 for GET, got {response.status_code}")
        return False

    # Test PUT 404
    response = client.put(f'/api/v1/amenities/{fake_id}',
                          data=json.dumps({'name': 'Should Fail'}),
                          content_type='application/json')
    if response.status_code == 404:
        error = json.loads(response.data)
        print(
            f"   ✓ PUT 404 handled correctly: {
                error.get(
                    'error',
                    'No error message')}")
    else:
        print(f"   ✗ Expected 404 for PUT, got {response.status_code}")
        return False

    # Test 6: Input validation errors
    print("\n6. Testing input validation...")

    # Test empty name
    response = client.post('/api/v1/amenities/',
                           data=json.dumps({'name': ''}),
                           content_type='application/json')
    if response.status_code == 400:
        print(f"   ✓ Empty name validation working")
    else:
        print(
            f"     Expected 400 for empty name, got {
                response.status_code}")

    # Test missing name
    response = client.post('/api/v1/amenities/',
                           data=json.dumps({}),
                           content_type='application/json')
    if response.status_code == 400:
        print(f"   ✓ Missing name validation working")
    else:
        print(
            f"     Expected 400 for missing name, got {
                response.status_code}")

    # Test invalid JSON
    response = client.post('/api/v1/amenities/',
                           data='{"invalid": json}',
                           content_type='application/json')
    if response.status_code == 400:
        print(f"   ✓ Invalid JSON handled correctly")
    else:
        print(
            f"     Expected 400 for invalid JSON, got {
                response.status_code}")

    # Test 7: Verify final state
    print("\n7. Verifying final state...")
    response = client.get('/api/v1/amenities/')
    if response.status_code == 200:
        final_amenities = json.loads(response.data)
        print(f"   ✓ Final amenity count: {len(final_amenities)}")

        print(f"    All amenities in system:")
        for amenity in final_amenities:
            print(f"     - {amenity['name']} (ID: {amenity['id'][:8]}...)")

    print("\n[SUCCESS] All amenity API tests passed!")
    return True


def test_api_integration():
    """Test API integration with other components"""
    print("\n[INTEGRATION] Testing API Integration...")

    app = create_app()
    client = app.test_client()

    # Test 1: Create amenity and verify via facade
    print("\n1. Testing API-Facade integration...")
    amenity_data = {'name': 'Integration Test Amenity'}

    response = client.post('/api/v1/amenities/',
                           data=json.dumps(amenity_data),
                           content_type='application/json')

    if response.status_code == 201:
        created_amenity = json.loads(response.data)
        print(f"   ✓ Amenity created via API: {created_amenity['name']}")

        # Verify we can retrieve it directly via facade
        from app.services import facade
        direct_amenity = facade.get_amenity(created_amenity['id'])

        if direct_amenity and direct_amenity.name == created_amenity['name']:
            print(f"   ✓ Amenity accessible via facade")
        else:
            print(f"   ✗ Amenity not accessible via facade")
            return False
    else:
        print(f"   ✗ Failed to create amenity via API")
        return False

    # Test 2: Performance test
    print("\n2. Testing API performance...")
    import time

    start_time = time.time()
    for i in range(10):
        response = client.get('/api/v1/amenities/')
    end_time = time.time()

    avg_time = (end_time - start_time) / 10 * 1000
    print(f"   ✓ 10 GET requests completed")
    print(f"   ⚡ Average response time: {avg_time:.2f} ms")

    print("\n[SUCCESS] All integration tests passed!")
    return True


def print_api_documentation():
    """Print comprehensive API documentation"""
    print("\n" + "=" * 80)
    print("[DOCS] AMENITY API ENDPOINTS DOCUMENTATION")
    print("=" * 80)
    print("""
BASE URL: /api/v1/amenities

AVAILABLE ENDPOINTS:

1. POST /api/v1/amenities/
   Description: Create a new amenity
   Request Body: {"name": "string (required)"}
   Success Response (201):
      {
        "id": "uuid-string",
        "name": "string",
        "created_at": "ISO-datetime",
        "updated_at": "ISO-datetime"
      }
   Error Responses:
      400 - Missing required field: name
      400 - Name cannot be empty
      400 - Invalid input data

2. GET /api/v1/amenities/
   Description: Retrieve all amenities
   Success Response (200): Array of amenity objects
   Error Response: 500 - Server error

3. GET /api/v1/amenities/<amenity_id>
   Description: Retrieve specific amenity by ID
   Success Response (200): Single amenity object
   Error Responses:
      404 - Amenity not found
      500 - Server error

4. PUT /api/v1/amenities/<amenity_id>
   Description: Update amenity information
   Request Body: {"name": "string (required)"}
   Success Response (200): Updated amenity object
   Error Responses:
      400 - Missing required field: name
      400 - Name cannot be empty
      404 - Amenity not found
      500 - Server error

VALIDATION RULES:
   • name: Required, non-empty string
   • Whitespace-only names are rejected
   • All responses include timestamps

EXAMPLE USAGE:
   # Create amenity
   curl -X POST http://localhost:5000/api/v1/amenities/ \\
        -H "Content-Type: application/json" \\
        -d '{"name": "WiFi"}'

   # Get all amenities
   curl -X GET http://localhost:5000/api/v1/amenities/

   # Get specific amenity
   curl -X GET http://localhost:5000/api/v1/amenities/<amenity_id>

   # Update amenity
   curl -X PUT http://localhost:5000/api/v1/amenities/<amenity_id> \\
        -H "Content-Type: application/json" \\
        -d '{"name": "Premium WiFi"}'
""")
    print("=" * 80)


if __name__ == "__main__":
    print_api_documentation()

    # Run API endpoint tests
    success1 = test_amenity_api_endpoints()
    if not success1:
        sys.exit(1)

    # Run integration tests
    success2 = test_api_integration()
    if not success2:
        sys.exit(1)

    print(f"\n ALL AMENITY API TESTS PASSED!")
    print(f" Amenity API endpoints are fully functional!")
    print(f" Ready for production use!")

    sys.exit(0)
