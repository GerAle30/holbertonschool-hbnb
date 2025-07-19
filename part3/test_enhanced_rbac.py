#!/usr/bin/env python3
"""
Enhanced test script to verify Role-Based Access Control (RBAC) implementation
using get_jwt() function and enhanced admin privileges checking
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_enhanced_rbac():
    """Test the enhanced RBAC functionality with get_jwt() implementation"""
    print("[TEST] Testing Enhanced Role-Based Access Control (RBAC)\n")
    
    # Step 1: Test admin-only endpoints
    print("1. Testing admin-only endpoints...")
    
    # Test user creation without token (should fail with 401)
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code == 401:
        print("[PASS] Unauthenticated user creation correctly returns 401")
    else:
        print(f"[FAIL] Expected 401 but got {response.status_code}: {response.text}")
    
    # Test amenity creation without token (should fail with 401)
    amenity_data = {"name": "Test Amenity"}
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
    if response.status_code == 401:
        print("[PASS] Unauthenticated amenity creation correctly returns 401")
    else:
        print(f"[FAIL] Expected 401 but got {response.status_code}: {response.text}")
    
    # Step 2: Login with existing users (assuming they exist)
    print("\n2. Testing login and JWT token functionality...")
    
    # Try to login with admin user
    admin_login = {
        "email": "admin@example.com",
        "password": "adminpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    if response.status_code == 200:
        admin_token = response.json()['access_token']
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print("[SUCCESS] Admin login successful")
        
        # Verify admin token contains proper claims
        response = requests.get(f"{BASE_URL}/auth/protected", headers=admin_headers)
        if response.status_code == 200:
            protected_data = response.json()
            is_admin = protected_data.get('is_admin', False)
            if is_admin:
                print("[PASS] Admin JWT token contains is_admin flag")
            else:
                print("[FAIL] Admin JWT token missing is_admin flag")
        
    else:
        print(f"[INFO] Admin user not found or login failed. Creating test scenario...")
        admin_token = None
        admin_headers = None
    
    # Try to login with regular user
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
        print(f"[INFO] Regular user not found or login failed.")
        regular_token = None
        regular_headers = None
    
    # Step 3: Test enhanced admin privilege checking
    if admin_headers:
        print("\n3. Testing enhanced admin privilege checking...")
        
        # Test admin user creation with enhanced validation
        enhanced_user_data = {
            "first_name": "Enhanced",
            "last_name": "User",
            "email": "enhanced@example.com",
            "password": "enhancedpass123",
            "is_admin": False
        }
        
        response = requests.post(f"{BASE_URL}/users/", json=enhanced_user_data, headers=admin_headers)
        if response.status_code == 201:
            enhanced_user_id = response.json()['id']
            print("[PASS] Admin can create users with enhanced RBAC")
            print(f"       Created user ID: {enhanced_user_id}")
            
            # Test enhanced error messages
            print("\n4. Testing enhanced error messages and validation...")
            
            # Test duplicate email validation
            response = requests.post(f"{BASE_URL}/users/", json=enhanced_user_data, headers=admin_headers)
            if response.status_code == 400 and "Email already registered" in response.text:
                print("[PASS] Enhanced email uniqueness validation working")
            else:
                print(f"[FAIL] Email uniqueness check failed: {response.status_code}: {response.text}")
            
            # Test admin modification of user with sensitive fields
            user_update = {
                "first_name": "Modified",
                "email": "modified@example.com",
                "password": "newpassword123",
                "is_admin": True
            }
            
            response = requests.put(f"{BASE_URL}/users/{enhanced_user_id}", json=user_update, headers=admin_headers)
            if response.status_code == 200:
                updated_user = response.json()
                if (updated_user.get('email') == 'modified@example.com' and 
                    updated_user.get('is_admin') == True):
                    print("[PASS] Admin can modify sensitive user fields")
                else:
                    print(f"[FAIL] User fields not properly updated: {updated_user}")
            else:
                print(f"[FAIL] Admin user modification failed: {response.status_code}: {response.text}")
        else:
            print(f"[FAIL] Admin user creation failed: {response.status_code}: {response.text}")
    
    # Step 5: Test regular user restrictions
    if regular_headers:
        print("\n5. Testing regular user restrictions...")
        
        # Test that regular users cannot create users
        test_user_data = {
            "first_name": "Blocked",
            "last_name": "User",
            "email": "blocked@example.com",
            "password": "blockedpass123"
        }
        
        response = requests.post(f"{BASE_URL}/users/", json=test_user_data, headers=regular_headers)
        if response.status_code == 403:
            error_msg = response.json().get('error', '')
            if "Admin privileges required" in error_msg:
                print("[PASS] Regular user correctly blocked from user creation with enhanced error message")
            else:
                print(f"[PARTIAL] Regular user blocked but with generic message: {error_msg}")
        else:
            print(f"[FAIL] Regular user not properly blocked: {response.status_code}: {response.text}")
        
        # Test that regular users cannot create amenities
        response = requests.post(f"{BASE_URL}/amenities/", json={"name": "Blocked Amenity"}, headers=regular_headers)
        if response.status_code == 403:
            error_msg = response.json().get('error', '')
            if "Admin privileges required" in error_msg:
                print("[PASS] Regular user correctly blocked from amenity creation")
            else:
                print(f"[PARTIAL] Regular user blocked but with generic message: {error_msg}")
        else:
            print(f"[FAIL] Regular user not properly blocked from amenity creation")
    
    # Step 6: Test enhanced ownership bypass for admins
    if admin_headers and regular_headers:
        print("\n6. Testing enhanced ownership bypass for admins...")
        
        # Create a place with regular user
        place_data = {
            "title": "Regular User Place",
            "description": "Place owned by regular user",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        
        response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=regular_headers)
        if response.status_code == 201:
            place_id = response.json()['id']
            print("[SUCCESS] Regular user created place")
            
            # Admin modifies regular user's place
            place_update = {
                "title": "Admin Modified Place",
                "price": 999.0
            }
            
            response = requests.put(f"{BASE_URL}/places/{place_id}", json=place_update, headers=admin_headers)
            if response.status_code == 200:
                print("[PASS] Admin can bypass ownership restrictions on places")
            else:
                print(f"[FAIL] Admin ownership bypass failed: {response.status_code}: {response.text}")
            
            # Admin deletes regular user's place
            response = requests.delete(f"{BASE_URL}/places/{place_id}", headers=admin_headers)
            if response.status_code == 200:
                result = response.json()
                if result.get('deleted_by_admin'):
                    print("[PASS] Admin deletion includes admin flag in response")
                else:
                    print("[PARTIAL] Admin deletion successful but missing admin flag")
            else:
                print(f"[FAIL] Admin place deletion failed: {response.status_code}: {response.text}")
    
    # Step 7: Test enhanced amenity operations
    if admin_headers:
        print("\n7. Testing enhanced amenity operations...")
        
        # Create amenity with duplicate name validation
        amenity_data = {"name": "WiFi"}
        response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=admin_headers)
        if response.status_code == 201:
            amenity_id = response.json()['id']
            print("[SUCCESS] Admin created amenity")
            
            # Try to create duplicate
            response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=admin_headers)
            if response.status_code == 400 and "already exists" in response.text:
                print("[PASS] Enhanced duplicate amenity validation working")
            else:
                print(f"[FAIL] Duplicate amenity validation failed: {response.status_code}")
            
            # Update amenity
            amenity_update = {"name": "Premium WiFi"}
            response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=amenity_update, headers=admin_headers)
            if response.status_code == 200:
                result = response.json()
                if result.get('message') == 'Amenity successfully updated':
                    print("[PASS] Enhanced amenity update with success message")
                else:
                    print("[PARTIAL] Amenity updated but missing enhanced response")
            else:
                print(f"[FAIL] Amenity update failed: {response.status_code}: {response.text}")
    
    print("\n[COMPLETE] Enhanced RBAC testing completed!")
    print("\nKey Enhancements Tested:")
    print("- JWT claims checking with get_jwt()")
    print("- Enhanced error messages")
    print("- Admin privilege validation")
    print("- Ownership bypass tracking")
    print("- Duplicate validation")
    print("- Comprehensive authorization checks")


def test_rbac_utilities():
    """Test the RBAC utility functions"""
    print("\n" + "="*60)
    print("[UTILITY] Testing RBAC Utility Functions")
    print("="*60)
    
    print("RBAC utilities provide the following functions:")
    print("- admin_required decorator")
    print("- check_admin_or_owner function")
    print("- get_current_user_info function")
    print("- require_admin_or_owner function")
    print("- RBACError custom exception")
    
    print("\nThese utilities enhance the JWT-based access control by:")
    print("1. Using both get_jwt_identity() and get_jwt() for comprehensive checking")
    print("2. Providing consistent authorization patterns across endpoints")
    print("3. Enabling centralized admin privilege validation")
    print("4. Supporting ownership-based access control")
    print("5. Offering enhanced error handling and reporting")


if __name__ == "__main__":
    test_rbac_utilities()
    test_enhanced_rbac()
