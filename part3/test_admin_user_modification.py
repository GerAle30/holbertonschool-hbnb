#!/usr/bin/env python3
"""
Test script to verify enhanced admin user modification functionality
Tests the PUT /api/v1/users/<user_id> endpoint for admin modifications
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_user_modification():
    """Test admin user modification with comprehensive scenarios"""
    print("[TEST] Testing Admin User Modification Functionality\n")
    
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
    
    # Step 2: Login as regular user for comparison
    print("\n2. Logging in as regular user...")
    regular_login = {
        "email": "regular@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=regular_login)
    if response.status_code == 200:
        regular_token = response.json()['access_token']
        regular_headers = {"Authorization": f"Bearer {regular_token}"}
        regular_user_data = response.json()
        regular_user_id = regular_user_data.get('user_id')
        print("[SUCCESS] Regular user login successful")
    else:
        print(f"[INFO] Regular user not found, will create test user")
        regular_headers = None
        regular_user_id = None
    
    # Step 3: Create a test user for modification
    print("\n3. Creating test user for modification...")
    test_user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "testpass123",
        "is_admin": False
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=test_user_data, headers=admin_headers)
    if response.status_code == 201:
        test_user = response.json()
        test_user_id = test_user['id']
        print(f"[SUCCESS] Test user created with ID: {test_user_id}")
    else:
        print(f"[FAIL] Test user creation failed: {response.status_code}: {response.text}")
        return
    
    # Step 4: Test admin modification of email (should succeed)
    print("\n4. Testing admin email modification...")
    email_update = {
        "email": "modified@example.com"
    }
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=email_update, headers=admin_headers)
    if response.status_code == 200:
        result = response.json()
        if result.get('email') == 'modified@example.com':
            print("[PASS] Admin successfully modified user email")
            if result.get('modified_by_admin'):
                print("[PASS] Admin modification flag included in response")
            else:
                print("[PARTIAL] Email updated but missing admin flag")
        else:
            print(f"[FAIL] Email not properly updated: {result}")
    else:
        print(f"[FAIL] Admin email modification failed: {response.status_code}: {response.text}")
    
    # Step 5: Test admin modification of password (should succeed)
    print("\n5. Testing admin password modification...")
    password_update = {
        "password": "newadminpassword123"
    }
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=password_update, headers=admin_headers)
    if response.status_code == 200:
        result = response.json()
        if result.get('modified_by_admin'):
            print("[PASS] Admin successfully modified user password")
        else:
            print("[PARTIAL] Password updated but missing admin modification indicator")
    else:
        print(f"[FAIL] Admin password modification failed: {response.status_code}: {response.text}")
    
    # Step 6: Test email uniqueness validation
    print("\n6. Testing email uniqueness validation...")
    duplicate_email_update = {
        "email": "admin@example.com"  # Try to use admin's email
    }
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=duplicate_email_update, headers=admin_headers)
    if response.status_code == 400 and "Email already in use" in response.text:
        print("[PASS] Email uniqueness validation working correctly")
    else:
        print(f"[FAIL] Email uniqueness validation failed: {response.status_code}: {response.text}")
    
    # Step 7: Test admin modification of admin status
    print("\n7. Testing admin modification of admin status...")
    admin_status_update = {
        "is_admin": True
    }
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=admin_status_update, headers=admin_headers)
    if response.status_code == 200:
        result = response.json()
        if result.get('is_admin') == True:
            print("[PASS] Admin successfully modified user admin status")
        else:
            print(f"[FAIL] Admin status not properly updated: {result}")
    else:
        print(f"[FAIL] Admin status modification failed: {response.status_code}: {response.text}")
    
    # Step 8: Test comprehensive admin modification (multiple fields)
    print("\n8. Testing comprehensive admin modification...")
    comprehensive_update = {
        "first_name": "AdminModified",
        "last_name": "ComprehensiveUser",
        "email": "comprehensive@example.com",
        "password": "comprehensivepass123",
        "is_admin": False
    }
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=comprehensive_update, headers=admin_headers)
    if response.status_code == 200:
        result = response.json()
        success_checks = [
            result.get('first_name') == 'AdminModified',
            result.get('last_name') == 'ComprehensiveUser',
            result.get('email') == 'comprehensive@example.com',
            result.get('is_admin') == False,
            result.get('modified_by_admin') == True
        ]
        
        if all(success_checks):
            print("[PASS] Comprehensive admin modification successful")
        else:
            print(f"[PARTIAL] Some fields not properly updated: {result}")
    else:
        print(f"[FAIL] Comprehensive modification failed: {response.status_code}: {response.text}")
    
    # Step 9: Test regular user attempting sensitive field modification (should fail)
    if regular_headers:
        print("\n9. Testing regular user restrictions...")
        restricted_update = {
            "email": "hacker@example.com",
            "is_admin": True
        }
        
        response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=restricted_update, headers=regular_headers)
        if response.status_code == 403:
            error_msg = response.json().get('error', '')
            if "Admin privileges required" in error_msg or "Unauthorized" in error_msg:
                print("[PASS] Regular user correctly blocked from modifying other users")
            else:
                print(f"[PARTIAL] User blocked but with generic message: {error_msg}")
        else:
            print(f"[FAIL] Regular user not properly blocked: {response.status_code}")
    
    # Step 10: Test modification of non-existent user
    print("\n10. Testing modification of non-existent user...")
    fake_user_id = "00000000-0000-0000-0000-000000000000"
    fake_update = {
        "first_name": "NonExistent"
    }
    
    response = requests.put(f"{BASE_URL}/users/{fake_user_id}", json=fake_update, headers=admin_headers)
    if response.status_code == 404:
        print("[PASS] Non-existent user modification correctly returns 404")
    else:
        print(f"[FAIL] Non-existent user handling failed: {response.status_code}")
    
    # Step 11: Test empty data modification
    print("\n11. Testing empty data modification...")
    empty_update = {}
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=empty_update, headers=admin_headers)
    if response.status_code == 400:
        error_msg = response.json().get('error', '')
        if "No valid data provided" in error_msg or "No data provided" in error_msg:
            print("[PASS] Empty data modification correctly rejected")
        else:
            print(f"[PARTIAL] Empty data rejected but with different message: {error_msg}")
    else:
        print(f"[FAIL] Empty data modification not properly handled: {response.status_code}")
    
    # Cleanup: Delete test user
    print("\n12. Cleaning up test user...")
    response = requests.delete(f"{BASE_URL}/users/{test_user_id}", headers=admin_headers)
    if response.status_code == 200:
        print("[SUCCESS] Test user cleaned up")
    else:
        print(f"[INFO] Test user cleanup failed: {response.status_code}")
    
    print("\n[COMPLETE] Admin User Modification Testing Completed!")
    print("\nKey Features Tested:")
    print("- Admin can modify any user field including email and password")
    print("- Email uniqueness validation prevents duplicates")
    print("- Admin modification tracking in responses")
    print("- Regular user restrictions on sensitive fields")
    print("- Proper error handling for edge cases")
    print("- Authorization checks for user ownership vs admin privileges")


if __name__ == "__main__":
    test_admin_user_modification()
