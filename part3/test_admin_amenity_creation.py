#!/usr/bin/env python3
"""
Test script to verify enhanced admin amenity creation functionality
Tests the POST /api/v1/amenities/ endpoint for admin-only amenity creation
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_amenity_creation():
    """Test admin amenity creation with comprehensive scenarios"""
    print("[TEST] Testing Admin Amenity Creation Functionality\n")
    
    # Step 1: Test unauthenticated access (should fail)
    print("1. Testing unauthenticated amenity creation...")
    amenity_data = {"name": "Unauthorized WiFi"}
    
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
    if response.status_code == 401:
        print("[PASS] Unauthenticated request correctly returns 401")
    else:
        print(f"[FAIL] Expected 401 but got {response.status_code}: {response.text}")
    
    # Step 2: Login as admin
    print("\n2. Logging in as administrator...")
    admin_login = {
        "email": "admin@example.com",
        "password": "adminpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    if response.status_code == 200:
        admin_token = response.json()['access_token']
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print("[SUCCESS] Admin login successful")
    else:
        print(f"[FAIL] Admin login failed: {response.status_code}")
        return
    
    # Step 3: Login as regular user for comparison
    print("\n3. Logging in as regular user...")
    regular_login = {
        "email": "regular@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=regular_login)
    if response.status_code == 200:
        regular_token = response.json()['access_token']
        regular_headers = {"Authorization": f"Bearer {regular_token}"}
        print("[SUCCESS] Regular user login successful")
    else:
        print(f"[INFO] Regular user not found, will skip regular user tests")
        regular_headers = None
    
    # Step 4: Test regular user attempting to create amenity (should fail)
    if regular_headers:
        print("\n4. Testing regular user amenity creation restriction...")
        blocked_amenity = {"name": "Blocked WiFi"}
        
        response = requests.post(f"{BASE_URL}/amenities/", json=blocked_amenity, headers=regular_headers)
        if response.status_code == 403:
            error_msg = response.json().get('error', '')
            if "Admin privileges required" in error_msg:
                print("[PASS] Regular user correctly blocked from creating amenities")
            else:
                print(f"[PARTIAL] User blocked but with generic message: {error_msg}")
        else:
            print(f"[FAIL] Regular user not properly blocked: {response.status_code}")
    
    # Step 5: Test admin creating amenity successfully
    print("\n5. Testing admin amenity creation...")
    test_amenity = {"name": "Premium WiFi"}
    
    response = requests.post(f"{BASE_URL}/amenities/", json=test_amenity, headers=admin_headers)
    if response.status_code == 201:
        created_amenity = response.json()
        amenity_id = created_amenity.get('id')
        print(f"[SUCCESS] Admin created amenity with ID: {amenity_id}")
        
        # Check response structure
        required_fields = ['id', 'name', 'created_at', 'updated_at', 'message']
        missing_fields = [field for field in required_fields if field not in created_amenity]
        
        if not missing_fields:
            print("[PASS] Response contains all required fields")
        else:
            print(f"[PARTIAL] Missing fields in response: {missing_fields}")
        
        # Check admin creation flag
        if created_amenity.get('created_by_admin'):
            print("[PASS] Admin creation flag included in response")
        else:
            print("[PARTIAL] Admin creation flag missing from response")
            
    else:
        print(f"[FAIL] Admin amenity creation failed: {response.status_code}: {response.text}")
        return
    
    # Step 6: Test duplicate amenity name prevention
    print("\n6. Testing duplicate amenity name prevention...")
    duplicate_amenity = {"name": "Premium WiFi"}  # Same name as above
    
    response = requests.post(f"{BASE_URL}/amenities/", json=duplicate_amenity, headers=admin_headers)
    if response.status_code == 400:
        error_msg = response.json().get('error', '')
        if "already exists" in error_msg:
            print("[PASS] Duplicate amenity name correctly rejected")
        else:
            print(f"[PARTIAL] Duplicate rejected but with unexpected message: {error_msg}")
    else:
        print(f"[FAIL] Duplicate amenity name not properly handled: {response.status_code}")
    
    # Step 7: Test case-insensitive duplicate prevention
    print("\n7. Testing case-insensitive duplicate prevention...")
    case_duplicate = {"name": "PREMIUM WIFI"}  # Different case
    
    response = requests.post(f"{BASE_URL}/amenities/", json=case_duplicate, headers=admin_headers)
    if response.status_code == 400:
        error_msg = response.json().get('error', '')
        if "already exists" in error_msg:
            print("[PASS] Case-insensitive duplicate prevention working")
        else:
            print(f"[PARTIAL] Case-insensitive duplicate rejected with message: {error_msg}")
    else:
        print(f"[FAIL] Case-insensitive duplicate not properly handled: {response.status_code}")
    
    # Step 8: Test whitespace handling
    print("\n8. Testing whitespace handling...")
    whitespace_amenity = {"name": "  Pool Area  "}  # Leading/trailing whitespace
    
    response = requests.post(f"{BASE_URL}/amenities/", json=whitespace_amenity, headers=admin_headers)
    if response.status_code == 201:
        created_amenity = response.json()
        if created_amenity.get('name') == 'Pool Area':
            print("[PASS] Whitespace correctly trimmed from amenity name")
        else:
            print(f"[PARTIAL] Amenity created but name not properly trimmed: '{created_amenity.get('name')}'")
    else:
        print(f"[FAIL] Whitespace amenity creation failed: {response.status_code}: {response.text}")
    
    # Step 9: Test empty name validation
    print("\n9. Testing empty name validation...")
    empty_name_tests = [
        {"name": ""},           # Empty string
        {"name": "   "},        # Whitespace only
        {},                     # Missing name field
        {"name": None}          # Null name
    ]
    
    for i, empty_test in enumerate(empty_name_tests):
        response = requests.post(f"{BASE_URL}/amenities/", json=empty_test, headers=admin_headers)
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            print(f"[PASS] Empty name test {i+1} correctly rejected: {error_msg}")
        else:
            print(f"[FAIL] Empty name test {i+1} not properly handled: {response.status_code}")
    
    # Step 10: Test no data provided
    print("\n10. Testing no data validation...")
    response = requests.post(f"{BASE_URL}/amenities/", headers=admin_headers)  # No JSON data
    if response.status_code == 400:
        error_msg = response.json().get('error', '')
        if "No data provided" in error_msg:
            print("[PASS] No data validation working correctly")
        else:
            print(f"[PARTIAL] No data rejected with message: {error_msg}")
    else:
        print(f"[FAIL] No data scenario not properly handled: {response.status_code}")
    
    # Step 11: Test special characters in amenity names
    print("\n11. Testing special characters in amenity names...")
    special_amenities = [
        {"name": "WiFi & Internet"},
        {"name": "24/7 Gym Access"},
        {"name": "Air Conditioning (AC)"},
        {"name": "Pet-Friendly Amenity"}
    ]
    
    created_special_ids = []
    for special_amenity in special_amenities:
        response = requests.post(f"{BASE_URL}/amenities/", json=special_amenity, headers=admin_headers)
        if response.status_code == 201:
            amenity_id = response.json().get('id')
            created_special_ids.append(amenity_id)
            print(f"[PASS] Special character amenity created: '{special_amenity['name']}'")
        else:
            print(f"[FAIL] Special character amenity failed: {response.status_code}")
    
    # Step 12: Test retrieving all amenities
    print("\n12. Testing amenity retrieval...")
    response = requests.get(f"{BASE_URL}/amenities/")
    if response.status_code == 200:
        amenities = response.json()
        if isinstance(amenities, list) and len(amenities) > 0:
            print(f"[SUCCESS] Retrieved {len(amenities)} amenities")
            
            # Check if our created amenities are in the list
            amenity_names = [amenity.get('name') for amenity in amenities]
            if 'Premium WiFi' in amenity_names:
                print("[PASS] Created amenity found in list")
            else:
                print("[PARTIAL] Created amenity not found in list")
        else:
            print("[FAIL] No amenities retrieved or invalid format")
    else:
        print(f"[FAIL] Amenity retrieval failed: {response.status_code}")
    
    # Cleanup: Delete test amenities (if delete endpoint exists)
    print("\n13. Cleaning up test amenities...")
    cleanup_ids = [amenity_id] + created_special_ids
    for cleanup_id in cleanup_ids:
        if cleanup_id:
            response = requests.delete(f"{BASE_URL}/amenities/{cleanup_id}", headers=admin_headers)
            if response.status_code in [200, 204]:
                print(f"[SUCCESS] Cleaned up amenity {cleanup_id}")
            else:
                print(f"[INFO] Cleanup failed for amenity {cleanup_id}: {response.status_code}")
    
    print("\n[COMPLETE] Admin Amenity Creation Testing Completed!")
    print("\nKey Features Tested:")
    print("- Admin-only access control with JWT verification")
    print("- Enhanced admin privilege checking using get_jwt()")
    print("- Comprehensive input validation and sanitization")
    print("- Duplicate name prevention (case-insensitive)")
    print("- Whitespace handling and name cleaning")
    print("- Special character support in amenity names")
    print("- Proper error handling and informative messages")
    print("- Admin creation tracking in responses")


if __name__ == "__main__":
    test_admin_amenity_creation()
