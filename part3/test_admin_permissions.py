#!/usr/bin/env python3
"""
Test script to verify Administrator Permissions implementation
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_permissions():
    """Test the administrator permissions functionality"""
    print("[TEST] Testing Administrator Permissions Implementation\n")
    
    # Step 1: Create an admin user (this will need to be done manually first time)
    print("1. Creating admin user...")
    admin_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "password": "adminpass123",
        "is_admin": True
    }
    
    # Try creating admin user - this might fail if authentication is required
    # We'll handle this in the next steps
    
    # Step 2: Create a regular user first (temporarily bypass admin requirement)
    print("\n2. Creating regular user...")
    regular_user_data = {
        "first_name": "Regular",
        "last_name": "User", 
        "email": "regular@example.com",
        "password": "password123",
        "is_admin": False
    }
    
    # We need to temporarily create users without admin restriction for initial setup
    print("[INFO] For initial setup, you may need to temporarily remove admin restrictions")
    
    # Step 3: Test login for both users
    print("\n3. Testing login functionality...")
    
    # Login with regular user
    login_data_regular = {
        "email": "regular@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data_regular)
    if response.status_code == 200:
        regular_token = response.json()['access_token']
        regular_headers = {"Authorization": f"Bearer {regular_token}"}
        print("[SUCCESS] Regular user login successful")
    else:
        print(f"[FAIL] Regular user login failed: {response.text}")
        return
    
    # Login with admin user  
    login_data_admin = {
        "email": "admin@example.com", 
        "password": "adminpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data_admin)
    if response.status_code == 200:
        admin_token = response.json()['access_token'] 
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print("[SUCCESS] Admin user login successful")
    else:
        print(f"[FAIL] Admin user login failed: {response.text}")
        print("[INFO] You may need to manually create an admin user first")
        return
    
    # Step 4: Test restricted user creation (POST /api/v1/users/)
    print("\n4. Testing restricted user creation...")
    
    new_user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com", 
        "password": "testpass123"
    }
    
    # Regular user tries to create user (should fail)
    response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=regular_headers)
    if response.status_code == 403:
        print("[PASS] Regular user correctly blocked from creating users")
    else:
        print(f"[FAIL] Expected 403 but got {response.status_code}: {response.text}")
    
    # Admin user creates user (should succeed)
    response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=admin_headers)
    if response.status_code == 201:
        test_user_id = response.json()['id']
        print("[PASS] Admin user can create users")
    else:
        print(f"[FAIL] Admin user creation failed: {response.status_code}: {response.text}")
        return
    
    # Step 5: Test user modification permissions
    print("\n5. Testing user modification permissions...")
    
    # Regular user tries to modify admin fields on themselves (should fail)
    regular_user_update = {
        "first_name": "Updated",
        "email": "newemail@example.com",  # Should fail
        "is_admin": True  # Should fail
    }
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=regular_user_update, headers=regular_headers)
    if response.status_code == 400:
        print("[PASS] Regular user correctly blocked from modifying email/admin status")
    else:
        print(f"[FAIL] Expected 400 but got {response.status_code}: {response.text}")
    
    # Admin tries to modify user with all fields (should succeed)
    admin_user_update = {
        "first_name": "AdminUpdated",
        "email": "admin.updated@example.com",
        "password": "newpassword123",
        "is_admin": False
    }
    
    response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=admin_user_update, headers=admin_headers)
    if response.status_code == 200:
        print("[PASS] Admin user can modify all user fields")
    else:
        print(f"[FAIL] Admin user modification failed: {response.status_code}: {response.text}")
    
    # Step 6: Test amenity creation restrictions
    print("\n6. Testing amenity creation restrictions...")
    
    amenity_data = {
        "name": "Test Amenity"
    }
    
    # Regular user tries to create amenity (should fail)
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=regular_headers)
    if response.status_code == 403:
        print("[PASS] Regular user correctly blocked from creating amenities")
    else:
        print(f"[FAIL] Expected 403 but got {response.status_code}: {response.text}")
    
    # Admin user creates amenity (should succeed)
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=admin_headers)
    if response.status_code == 201:
        amenity_id = response.json()['id']
        print("[PASS] Admin user can create amenities")
    else:
        print(f"[FAIL] Admin amenity creation failed: {response.status_code}: {response.text}")
        return
    
    # Step 7: Test amenity modification restrictions
    print("\n7. Testing amenity modification restrictions...")
    
    amenity_update = {
        "name": "Updated Test Amenity"
    }
    
    # Regular user tries to update amenity (should fail)
    response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=amenity_update, headers=regular_headers)
    if response.status_code == 403:
        print("[PASS] Regular user correctly blocked from updating amenities")
    else:
        print(f"[FAIL] Expected 403 but got {response.status_code}: {response.text}")
    
    # Admin user updates amenity (should succeed) 
    response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=amenity_update, headers=admin_headers)
    if response.status_code == 200:
        print("[PASS] Admin user can update amenities")
    else:
        print(f"[FAIL] Admin amenity update failed: {response.status_code}: {response.text}")
    
    # Step 8: Test admin bypass of place ownership restrictions
    print("\n8. Testing admin bypass of place ownership restrictions...")
    
    # Create a place with regular user
    place_data = {
        "title": "Regular User Place",
        "description": "A place owned by regular user",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=regular_headers)
    if response.status_code == 201:
        place_id = response.json()['id']
        print("[SUCCESS] Regular user created place")
        
        # Admin tries to modify regular user's place (should succeed)
        place_update = {
            "title": "Admin Modified Place",
            "price": 200.0
        }
        
        response = requests.put(f"{BASE_URL}/places/{place_id}", json=place_update, headers=admin_headers)
        if response.status_code == 200:
            print("[PASS] Admin user can modify any user's place")
        else:
            print(f"[FAIL] Admin place modification failed: {response.status_code}: {response.text}")
            
        # Admin tries to delete regular user's place (should succeed)
        response = requests.delete(f"{BASE_URL}/places/{place_id}", headers=admin_headers)
        if response.status_code == 200:
            print("[PASS] Admin user can delete any user's place")
        else:
            print(f"[FAIL] Admin place deletion failed: {response.status_code}: {response.text}")
    else:
        print(f"[FAIL] Regular user place creation failed: {response.status_code}: {response.text}")
    
    # Step 9: Test admin bypass of review ownership restrictions
    print("\n9. Testing admin bypass of review ownership restrictions...")
    
    # Create another place for testing reviews
    place_data2 = {
        "title": "Review Test Place",
        "description": "A place for review testing",
        "price": 150.0,
        "latitude": 34.0522,
        "longitude": -118.2437
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data2, headers=admin_headers)
    if response.status_code == 201:
        place2_id = response.json()['id']
        
        # Regular user creates review
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": test_user_id,  # Using the created test user
            "place_id": place2_id
        }
        
        # First login as the test user to create review
        login_test_user = {
            "email": "admin.updated@example.com",  # Updated email from step 5
            "password": "newpassword123"  # Updated password from step 5
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_test_user)
        if response.status_code == 200:
            test_user_token = response.json()['access_token']
            test_user_headers = {"Authorization": f"Bearer {test_user_token}"}
            
            response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=test_user_headers)
            if response.status_code == 201:
                review_id = response.json()['id']
                print("[SUCCESS] Test user created review")
                
                # Admin tries to modify test user's review (should succeed)
                review_update = {
                    "text": "Admin modified this review",
                    "rating": 3,
                    "user_id": test_user_id,
                    "place_id": place2_id
                }
                
                response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=review_update, headers=admin_headers)
                if response.status_code == 200:
                    print("[PASS] Admin user can modify any user's review")
                else:
                    print(f"[FAIL] Admin review modification failed: {response.status_code}: {response.text}")
                
                # Admin tries to delete test user's review (should succeed)
                response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=admin_headers)
                if response.status_code == 200:
                    print("[PASS] Admin user can delete any user's review")
                else:
                    print(f"[FAIL] Admin review deletion failed: {response.status_code}: {response.text}")
            else:
                print(f"[FAIL] Test user review creation failed: {response.status_code}: {response.text}")
        else:
            print(f"[FAIL] Test user login failed: {response.status_code}: {response.text}")
    else:
        print(f"[FAIL] Admin place creation for review test failed: {response.status_code}: {response.text}")
    
    print("\n[COMPLETE] Administrator permissions testing completed!")


def setup_instructions():
    """Print setup instructions for admin permissions testing"""
    print("\n" + "="*60)
    print("[SETUP] Administrator Permissions Setup Instructions")
    print("="*60)
    print("""
To test administrator permissions, you need to set up an initial admin user.

Since user creation is now restricted to admins, you have a few options:

1. TEMPORARY BYPASS (Recommended for initial setup):
   - Temporarily comment out the admin check in user.py POST method
   - Create an admin user manually
   - Re-enable the admin check

2. DATABASE/REPOSITORY SETUP:
   - Manually add an admin user directly to your data store
   - Set is_admin=True for this user

3. CONFIGURATION FLAG:
   - Add a configuration option to allow initial admin user creation

Example admin user data:
{
    "first_name": "Admin",
    "last_name": "User", 
    "email": "admin@example.com",
    "password": "adminpass123",
    "is_admin": true
}

After creating the admin user, run this test script to verify permissions.
""")
    print("="*60)


if __name__ == "__main__":
    setup_instructions()
    test_admin_permissions()
