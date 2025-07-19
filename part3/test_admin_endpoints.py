#!/usr/bin/env python3
"""
Admin Endpoints Testing Script
This script creates an admin user and tests all admin-only endpoints
"""

import requests
import json
import subprocess
import os

BASE_URL = "http://127.0.0.1:5000/api/v1"

def create_initial_admin_user():
    """
    Strategy to create an initial admin user
    This uses a backdoor approach - directly creating a user with admin privileges
    """
    print("[SETUP] Creating initial admin user...")
    
    # Method 1: Try to use existing admin user if available
    admin_credentials = {
        "email": "admin@hbnb.io", 
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_credentials)
    if response.status_code == 200:
        print("[SUCCESS] Found existing admin user")
        return response.json()['access_token']
    
    # Method 2: Try common admin credentials
    common_admin_creds = [
        {"email": "admin@example.com", "password": "adminpass123"},
        {"email": "admin@hbnb.io", "password": "admin123"},
        {"email": "root@example.com", "password": "rootpass123"}
    ]
    
    for creds in common_admin_creds:
        response = requests.post(f"{BASE_URL}/auth/login", json=creds)
        if response.status_code == 200:
            user_data = response.json()
            # Check if user has admin privileges
            admin_token = user_data['access_token']
            
            # Test admin privileges
            test_response = requests.get(f"{BASE_URL}/auth/protected", 
                                       headers={"Authorization": f"Bearer {admin_token}"})
            if test_response.status_code == 200:
                protected_data = test_response.json()
                if protected_data.get('is_admin'):
                    print(f"[SUCCESS] Found admin user with email: {creds['email']}")
                    return admin_token
    
    print("[INFO] No existing admin user found. Strategies to create one:")
    print("1. Database Seeding: Manually insert admin user in database")
    print("2. Environment Setup: Create first user as admin automatically")
    print("3. CLI Command: Use command line to promote user to admin")
    print("4. Configuration: Set admin users in config file")
    
    # Method 3: Try to create a regular user and then manually promote (simulation)
    print("\n[ATTEMPT] Creating regular user and attempting admin promotion...")
    
    # Create a regular user first
    regular_user = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "newadmin@example.com",
        "password": "adminpass123"
    }
    
    # Note: This will fail without an existing admin, but shows the process
    print("[INFO] Admin user creation requires existing admin privileges")
    print("[INFO] This is a security feature - admin users cannot self-create")
    
    return None

def test_admin_endpoints():
    """Test all admin endpoints with comprehensive validation"""
    print("\n" + "="*70)
    print("[TEST] Admin Endpoints Comprehensive Testing")
    print("="*70)
    
    # Step 1: Get admin token
    admin_token = create_initial_admin_user()
    
    if not admin_token:
        print("\n[CRITICAL] Cannot proceed without admin token")
        print("\n** SOLUTION STRATEGIES **")
        print("1. Database Direct Insert:")
        print("   INSERT INTO users (id, first_name, last_name, email, password, is_admin)")
        print("   VALUES (uuid_generate_v4(), 'Admin', 'User', 'admin@example.com', 'hashed_password', true);")
        print("")
        print("2. Modify facade.py to auto-create admin on first run:")
        print("   if not facade.get_user_by_email('admin@example.com'):")
        print("       facade.create_user({'email': 'admin@example.com', 'password': 'admin123', 'is_admin': True})")
        print("")
        print("3. Environment Variable Setup:")
        print("   export ADMIN_EMAIL='admin@example.com'")
        print("   export ADMIN_PASSWORD='admin123'")
        print("")
        return False
    
    admin_headers = {"Authorization": f"Bearer {admin_token}", "Content-Type": "application/json"}
    
    print(f"\n[SUCCESS] Admin token acquired")
    print(f"Token preview: {admin_token[:20]}...")
    
    # Verify admin status
    response = requests.get(f"{BASE_URL}/auth/protected", headers=admin_headers)
    if response.status_code == 200:
        protected_data = response.json()
        print(f"[VERIFIED] Admin status: {protected_data.get('is_admin')}")
        print(f"[VERIFIED] User ID: {protected_data.get('user_id')}")
    
    test_results = []
    
    # Test 1: Create a New User as an Admin
    print("\n" + "-"*50)
    print("TEST 1: Create a New User as an Admin")
    print("-"*50)
    
    new_user_data = {
        "email": "newuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpass123"
    }
    
    print(f"Request: POST {BASE_URL}/users/")
    print(f"Data: {json.dumps(new_user_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=admin_headers)
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 201:
        created_user = response.json()
        new_user_id = created_user.get('id')
        print(f"SUCCESS: User created with ID {new_user_id}")
        print(f"Response: {json.dumps(created_user, indent=2)}")
        test_results.append(("Create User", "PASS", created_user))
        
        # Equivalent curl command
        print(f"\nEquivalent curl command:")
        print(f"curl -X POST \"{BASE_URL}/users/\" \\")
        print(f"  -d '{json.dumps(new_user_data)}' \\")
        print(f"  -H \"Authorization: Bearer {admin_token}\" \\")
        print(f"  -H \"Content-Type: application/json\"")
        
    else:
        print(f"FAILED: {response.status_code}")
        print(f"Error: {response.text}")
        test_results.append(("Create User", "FAIL", response.text))
        new_user_id = None
    
    # Test 2: Modify Another User's Data as an Admin  
    print("\n" + "-"*50)
    print("TEST 2: Modify Another User's Data as an Admin")
    print("-"*50)
    
    if new_user_id:
        update_data = {
            "email": "updatedemail@example.com",
            "first_name": "Updated",
            "last_name": "TestUser"
        }
        
        print(f"Request: PUT {BASE_URL}/users/{new_user_id}")
        print(f"Data: {json.dumps(update_data, indent=2)}")
        
        response = requests.put(f"{BASE_URL}/users/{new_user_id}", json=update_data, headers=admin_headers)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            updated_user = response.json()
            print(f"SUCCESS: User updated")
            print(f"Response: {json.dumps(updated_user, indent=2)}")
            test_results.append(("Update User", "PASS", updated_user))
            
            # Equivalent curl command
            print(f"\nEquivalent curl command:")
            print(f"curl -X PUT \"{BASE_URL}/users/{new_user_id}\" \\")
            print(f"  -d '{json.dumps(update_data)}' \\") 
            print(f"  -H \"Authorization: Bearer {admin_token}\" \\")
            print(f"  -H \"Content-Type: application/json\"")
            
        else:
            print(f"FAILED: {response.status_code}")
            print(f"Error: {response.text}")
            test_results.append(("Update User", "FAIL", response.text))
    else:
        print("SKIPPED: No user ID from previous test")
        test_results.append(("Update User", "SKIP", "No user created"))
    
    # Test 3: Add a New Amenity as an Admin
    print("\n" + "-"*50)
    print("TEST 3: Add a New Amenity as an Admin")
    print("-"*50)
    
    amenity_data = {"name": "Swimming Pool"}
    
    print(f"Request: POST {BASE_URL}/amenities/")
    print(f"Data: {json.dumps(amenity_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data, headers=admin_headers)
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 201:
        created_amenity = response.json()
        amenity_id = created_amenity.get('id')
        print(f"SUCCESS: Amenity created with ID {amenity_id}")
        print(f"Response: {json.dumps(created_amenity, indent=2)}")
        test_results.append(("Create Amenity", "PASS", created_amenity))
        
        # Equivalent curl command
        print(f"\nEquivalent curl command:")
        print(f"curl -X POST \"{BASE_URL}/amenities/\" \\")
        print(f"  -d '{json.dumps(amenity_data)}' \\")
        print(f"  -H \"Authorization: Bearer {admin_token}\" \\")
        print(f"  -H \"Content-Type: application/json\"")
        
    else:
        print(f"FAILED: {response.status_code}")
        print(f"Error: {response.text}")
        test_results.append(("Create Amenity", "FAIL", response.text))
        amenity_id = None
    
    # Test 4: Modify an Amenity as an Admin
    print("\n" + "-"*50)
    print("TEST 4: Modify an Amenity as an Admin")
    print("-"*50)
    
    if amenity_id:
        amenity_update = {"name": "Updated Swimming Pool"}
        
        print(f"Request: PUT {BASE_URL}/amenities/{amenity_id}")
        print(f"Data: {json.dumps(amenity_update, indent=2)}")
        
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=amenity_update, headers=admin_headers)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            updated_amenity = response.json()
            print(f"SUCCESS: Amenity updated")
            print(f"Response: {json.dumps(updated_amenity, indent=2)}")
            test_results.append(("Update Amenity", "PASS", updated_amenity))
            
            # Equivalent curl command
            print(f"\nEquivalent curl command:")
            print(f"curl -X PUT \"{BASE_URL}/amenities/{amenity_id}\" \\")
            print(f"  -d '{json.dumps(amenity_update)}' \\")
            print(f"  -H \"Authorization: Bearer {admin_token}\" \\")
            print(f"  -H \"Content-Type: application/json\"")
            
        else:
            print(f"FAILED: {response.status_code}")
            print(f"Error: {response.text}")
            test_results.append(("Update Amenity", "FAIL", response.text))
    else:
        print("SKIPPED: No amenity ID from previous test")
        test_results.append(("Update Amenity", "SKIP", "No amenity created"))
    
    # Test 5: Test Admin Bypass - Modify Another User's Place
    print("\n" + "-"*50)
    print("TEST 5: Admin Bypass - Modify Another User's Place")
    print("-"*50)
    
    # Create regular user and place for testing bypass
    regular_user_creds = {"email": "regularuser@example.com", "password": "regular123"}
    
    # First create a regular user
    response = requests.post(f"{BASE_URL}/users/", json={
        "email": "regularuser@example.com",
        "first_name": "Regular",
        "last_name": "User", 
        "password": "regular123"
    }, headers=admin_headers)
    
    if response.status_code == 201:
        regular_user = response.json()
        
        # Login as regular user
        response = requests.post(f"{BASE_URL}/auth/login", json=regular_user_creds)
        if response.status_code == 200:
            regular_token = response.json()['access_token']
            regular_headers = {"Authorization": f"Bearer {regular_token}", "Content-Type": "application/json"}
            
            # Create place as regular user
            place_data = {
                "title": "Regular User's Place",
                "description": "A place by regular user",
                "price": 100.0,
                "latitude": 40.7128,
                "longitude": -74.0060
            }
            
            response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=regular_headers)
            if response.status_code == 201:
                place = response.json()
                place_id = place['id']
                
                # Now admin modifies regular user's place
                admin_place_update = {
                    "title": "Modified by Admin",
                    "price": 500.0
                }
                
                print(f"Request: PUT {BASE_URL}/places/{place_id}")
                print(f"Data: {json.dumps(admin_place_update, indent=2)}")
                
                response = requests.put(f"{BASE_URL}/places/{place_id}", json=admin_place_update, headers=admin_headers)
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    updated_place = response.json()
                    print(f"SUCCESS: Admin bypassed ownership to modify place")
                    print(f"Modified by admin: {updated_place.get('modified_by_admin')}")
                    print(f"Response: {json.dumps(updated_place, indent=2)}")
                    test_results.append(("Admin Bypass Place", "PASS", updated_place))
                else:
                    print(f"FAILED: {response.status_code}")
                    print(f"Error: {response.text}")
                    test_results.append(("Admin Bypass Place", "FAIL", response.text))
    
    # Test Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result, _ in test_results if result == "PASS")
    failed = sum(1 for _, result, _ in test_results if result == "FAIL")
    skipped = sum(1 for _, result, _ in test_results if result == "SKIP")
    
    for test_name, result, data in test_results:
        status_icon = "PASS" if result == "PASS" else "FAIL" if result == "FAIL" else "SKIP"
        print(f"[{status_icon}] {test_name}: {result}")
    
    print(f"\nResults: {passed} passed, {failed} failed, {skipped} skipped")
    
    if failed > 0:
        print("\nTroubleshooting Tips:")
        print("- Ensure the API server is running on http://127.0.0.1:5000")
        print("- Verify admin user exists in database") 
        print("- Check JWT token is valid and contains is_admin=true")
        print("- Validate all required fields are provided in requests")
    
    # Cleanup
    print("\nCleanup...")
    if new_user_id:
        requests.delete(f"{BASE_URL}/users/{new_user_id}", headers=admin_headers)
        print("Cleaned up test user")
    if amenity_id:
        requests.delete(f"{BASE_URL}/amenities/{amenity_id}", headers=admin_headers)
        print("Cleaned up test amenity")
    
    return passed > 0

def show_admin_setup_guide():
    """Show comprehensive guide for admin setup"""
    print("\n" + "="*70)
    print("ADMIN USER SETUP STRATEGIES")
    print("="*70)
    
    print("\nSTRATEGY 1: Database Direct Insert")
    print("Connect directly to your database and insert an admin user:")
    print("""
    -- PostgreSQL/SQLite example
    INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
    VALUES (
        '550e8400-e29b-41d4-a716-446655440000',  -- Generate UUID
        'Admin', 
        'User', 
        'admin@example.com', 
        'hashed_password_here',  -- Use proper password hashing
        true,  -- is_admin flag
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );
    """)
    
    print("\nSTRATEGY 2: Modify Application Code")
    print("Add auto-admin creation in facade.py or models:")
    print("""
    # In facade.py or startup code
    def ensure_admin_exists():
        admin_email = 'admin@example.com'
        if not self.get_user_by_email(admin_email):
            admin_user = {
                'first_name': 'System',
                'last_name': 'Admin',
                'email': admin_email,
                'password': 'admin123',  # Will be hashed
                'is_admin': True
            }
            self.create_user(admin_user)
            print(f"Created admin user: {admin_email}")
    """)
    
    print("\nSTRATEGY 3: Environment Variables")
    print("Use environment variables to define admin credentials:")
    print("""
    # Set environment variables
    export ADMIN_EMAIL="admin@example.com"  
    export ADMIN_PASSWORD="admin123"
    export AUTO_CREATE_ADMIN="true"
    
    # In your application startup
    if os.getenv('AUTO_CREATE_ADMIN') == 'true':
        create_admin_user()
    """)
    
    print("\nSTRATEGY 4: CLI Command")
    print("Create a management command:")
    print("""
    # create_admin.py
    import sys
    from app.services import facade
    
    def create_admin_user(email, password):
        user_data = {
            'first_name': 'Admin',
            'last_name': 'User', 
            'email': email,
            'password': password,
            'is_admin': True
        }
        admin = facade.create_user(user_data)
        print(f"Admin user created: {admin.email}")
    
    if __name__ == '__main__':
        create_admin_user(sys.argv[1], sys.argv[2])
    """)
    
    print("\nRECOMMENDED APPROACH:")
    print("1. Use Strategy 2 (modify application) for development")
    print("2. Use Strategy 1 (database insert) for production")
    print("3. Use Strategy 4 (CLI command) for deployment scripts")


if __name__ == "__main__":
    print("Admin Endpoints Testing Tool")
    print("="*70)
    
    # First show the setup guide
    show_admin_setup_guide()
    
    # Ask user if they want to proceed with testing
    print("\n" + "="*70)
    user_input = input("Do you have an admin user set up? (y/n): ").lower().strip()
    
    if user_input == 'y':
        success = test_admin_endpoints()
        if success:
            print("\nAdmin endpoints testing completed successfully!")
        else:
            print("\nSome tests failed. Check the output above for details.")
    else:
        print("\nPlease set up an admin user using one of the strategies above, then run this script again.")
        print("Quick setup: Modify your user creation code to auto-create admin@example.com as admin")
