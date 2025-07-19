#!/usr/bin/env python3
"""
Test script to verify enhanced admin amenity modification functionality
Tests the PUT /api/v1/amenities/<amenity_id> endpoint for admin-only amenity modification
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_amenity_modification():
    """Test admin amenity modification with comprehensive scenarios"""
    print("[TEST] Testing Admin Amenity Modification Functionality\n")
    
    # Step 1: Login as admin
    print("1. Logging in as administrator...")
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
    
    # Step 2: Login as regular user for testing restrictions
    print("\n2. Logging in as regular user...")
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
    
    # Step 3: Create test amenities for modification
    print("\n3. Creating test amenities for modification...")
    test_amenities = [
        {"name": "Original WiFi"},
        {"name": "Basic Pool"},
        {"name": "Standard Gym"}
    ]
    
    created_amenities = []
    for amenity_data in test_amenities:
        response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=admin_headers)
        if response.status_code == 201:
            amenity = response.json()
            created_amenities.append(amenity)
            print(f"[SUCCESS] Created amenity: {amenity['name']} (ID: {amenity['id']})")
        else:
            print(f"[FAIL] Failed to create amenity {amenity_data['name']}: {response.status_code}")
    
    if not created_amenities:
        print("[ERROR] No test amenities created, cannot continue with modification tests")
        return
    
    test_amenity = created_amenities[0]
    test_amenity_id = test_amenity['id']
    
    # Step 4: Test unauthenticated modification (should fail)
    print("\n4. Testing unauthenticated amenity modification...")
    update_data = {"name": "Unauthorized Update"}
    
    response = requests.put(f"{BASE_URL}/amenities/{test_amenity_id}", json=update_data)
    if response.status_code == 401:
        print("[PASS] Unauthenticated modification correctly returns 401")
    else:
        print(f"[FAIL] Expected 401 but got {response.status_code}: {response.text}")
    
    # Step 5: Test regular user modification restriction (should fail)
    if regular_headers:
        print("\n5. Testing regular user modification restriction...")
        blocked_update = {"name": "Regular User Blocked Update"}
        
        response = requests.put(f"{BASE_URL}/amenities/{test_amenity_id}", json=blocked_update, headers=regular_headers)
        if response.status_code == 403:
            error_msg = response.json().get('error', '')
            if "Admin privileges required" in error_msg:
                print("[PASS] Regular user correctly blocked from modifying amenities")
            else:
                print(f"[PARTIAL] User blocked but with generic message: {error_msg}")
        else:
            print(f"[FAIL] Regular user not properly blocked: {response.status_code}")
    
    # Step 6: Test admin amenity modification (should succeed)
    print("\n6. Testing admin amenity modification...")
    modification_data = {"name": "Modified Premium WiFi"}
    
    response = requests.put(f"{BASE_URL}/amenities/{test_amenity_id}", json=modification_data, headers=admin_headers)
    if response.status_code == 200:
        modified_amenity = response.json()
        if modified_amenity.get('name') == 'Modified Premium WiFi':
            print("[PASS] Admin successfully modified amenity name")
            
            # Check for admin modification flag
            if modified_amenity.get('modified_by_admin'):
                print("[PASS] Admin modification flag included in response")
            else:
                print("[PARTIAL] Amenity modified but missing admin flag")
            
            # Check response structure
            required_fields = ['id', 'name', 'created_at', 'updated_at', 'message']
            missing_fields = [field for field in required_fields if field not in modified_amenity]
            
            if not missing_fields:
                print("[PASS] Response contains all required fields")
            else:
                print(f"[PARTIAL] Missing fields in response: {missing_fields}")
        else:
            print(f"[FAIL] Amenity name not properly updated: {modified_amenity}")
    else:
        print(f"[FAIL] Admin amenity modification failed: {response.status_code}: {response.text}")
    
    # Step 7: Test duplicate name prevention during modification
    print("\n7. Testing duplicate name prevention during modification...")
    if len(created_amenities) > 1:
        second_amenity = created_amenities[1]
        duplicate_update = {"name": "Modified Premium WiFi"}  # Same as the first amenity's new name
        
        response = requests.put(f"{BASE_URL}/amenities/{second_amenity['id']}", json=duplicate_update, headers=admin_headers)
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            if "already exists" in error_msg:
                print("[PASS] Duplicate name prevention working during modification")
            else:
                print(f"[PARTIAL] Duplicate rejected with message: {error_msg}")
        else:
            print(f"[FAIL] Duplicate name not properly handled: {response.status_code}")
    
    # Step 8: Test case-insensitive duplicate prevention
    print("\n8. Testing case-insensitive duplicate prevention...")
    if len(created_amenities) > 1:
        second_amenity = created_amenities[1]
        case_duplicate = {"name": "MODIFIED PREMIUM WIFI"}  # Different case
        
        response = requests.put(f"{BASE_URL}/amenities/{second_amenity['id']}", json=case_duplicate, headers=admin_headers)
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            if "already exists" in error_msg:
                print("[PASS] Case-insensitive duplicate prevention working")
            else:
                print(f"[PARTIAL] Case-insensitive duplicate rejected: {error_msg}")
        else:
            print(f"[FAIL] Case-insensitive duplicate not properly handled: {response.status_code}")
    
    # Step 9: Test whitespace handling in modification
    print("\n9. Testing whitespace handling in modification...")
    if len(created_amenities) > 1:
        second_amenity = created_amenities[1]
        whitespace_update = {"name": "  Executive Pool  "}  # Leading/trailing whitespace
        
        response = requests.put(f"{BASE_URL}/amenities/{second_amenity['id']}", json=whitespace_update, headers=admin_headers)
        if response.status_code == 200:
            updated_amenity = response.json()
            if updated_amenity.get('name') == 'Executive Pool':
                print("[PASS] Whitespace correctly trimmed during modification")
            else:
                print(f"[PARTIAL] Modified but name not properly trimmed: '{updated_amenity.get('name')}'")
        else:
            print(f"[FAIL] Whitespace modification failed: {response.status_code}: {response.text}")
    
    # Step 10: Test empty/invalid name validation
    print("\n10. Testing empty/invalid name validation...")
    invalid_updates = [
        {"name": ""},           # Empty string
        {"name": "   "},        # Whitespace only
        {},                     # Missing name field
        {"name": None}          # Null name
    ]
    
    for i, invalid_update in enumerate(invalid_updates):
        response = requests.put(f"{BASE_URL}/amenities/{test_amenity_id}", json=invalid_update, headers=admin_headers)
        if response.status_code == 400:
            error_msg = response.json().get('error', '')
            print(f"[PASS] Invalid name test {i+1} correctly rejected: {error_msg}")
        else:
            print(f"[FAIL] Invalid name test {i+1} not properly handled: {response.status_code}")
    
    # Step 11: Test no data provided
    print("\n11. Testing no data validation...")
    response = requests.put(f"{BASE_URL}/amenities/{test_amenity_id}", headers=admin_headers)  # No JSON data
    if response.status_code == 400:
        error_msg = response.json().get('error', '')
        if "No data provided" in error_msg:
            print("[PASS] No data validation working correctly")
        else:
            print(f"[PARTIAL] No data rejected with message: {error_msg}")
    else:
        print(f"[FAIL] No data scenario not properly handled: {response.status_code}")
    
    # Step 12: Test modification of non-existent amenity
    print("\n12. Testing modification of non-existent amenity...")
    fake_amenity_id = "00000000-0000-0000-0000-000000000000"
    fake_update = {"name": "Non-Existent Amenity"}
    
    response = requests.put(f"{BASE_URL}/amenities/{fake_amenity_id}", json=fake_update, headers=admin_headers)
    if response.status_code == 404:
        error_msg = response.json().get('error', '')
        if "not found" in error_msg.lower():
            print("[PASS] Non-existent amenity modification correctly returns 404")
        else:
            print(f"[PARTIAL] 404 returned but with unexpected message: {error_msg}")
    else:
        print(f"[FAIL] Non-existent amenity handling failed: {response.status_code}")
    
    # Step 13: Test special characters in modified names
    print("\n13. Testing special characters in modified names...")
    if len(created_amenities) > 2:
        third_amenity = created_amenities[2]
        special_updates = [
            {"name": "Gym & Fitness Center"},
            {"name": "24/7 Access Pool"},
            {"name": "Premium WiFi (5G)"},
            {"name": "Pet-Friendly Area"}
        ]
        
        for special_update in special_updates:
            response = requests.put(f"{BASE_URL}/amenities/{third_amenity['id']}", json=special_update, headers=admin_headers)
            if response.status_code == 200:
                print(f"[PASS] Special character modification successful: '{special_update['name']}'")
                third_amenity = response.json()  # Update for next test
            else:
                print(f"[FAIL] Special character modification failed: {response.status_code}")
    
    # Step 14: Test retrieving modified amenities
    print("\n14. Testing retrieval of modified amenities...")
    response = requests.get(f"{BASE_URL}/amenities/")
    if response.status_code == 200:
        amenities = response.json()
        if isinstance(amenities, list):
            modified_names = [amenity.get('name') for amenity in amenities]
            if 'Modified Premium WiFi' in modified_names:
                print("[PASS] Modified amenity found in amenity list")
            else:
                print("[PARTIAL] Modified amenity not found in list")
            print(f"[SUCCESS] Retrieved {len(amenities)} amenities total")
        else:
            print("[FAIL] Invalid amenity list format")
    else:
        print(f"[FAIL] Amenity retrieval failed: {response.status_code}")
    
    # Cleanup: Delete test amenities
    print("\n15. Cleaning up test amenities...")
    for amenity in created_amenities:
        amenity_id = amenity.get('id')
        if amenity_id:
            response = requests.delete(f"{BASE_URL}/amenities/{amenity_id}", headers=admin_headers)
            if response.status_code in [200, 204]:
                print(f"[SUCCESS] Cleaned up amenity {amenity_id}")
            else:
                print(f"[INFO] Cleanup failed for amenity {amenity_id}: {response.status_code}")
    
    print("\n[COMPLETE] Admin Amenity Modification Testing Completed!")
    print("\nKey Features Tested:")
    print("- Admin-only access control with enhanced JWT verification")
    print("- Enhanced admin privilege checking using get_jwt()")
    print("- Comprehensive input validation and sanitization")
    print("- Duplicate name prevention during modification (case-insensitive)")
    print("- Whitespace handling and name cleaning")
    print("- Special character support in modified names")
    print("- Proper error handling for edge cases (404, 400, 403)")
    print("- Admin modification tracking in responses")
    print("- Validation of non-existent amenity modifications")


if __name__ == "__main__":
    test_admin_amenity_modification()
