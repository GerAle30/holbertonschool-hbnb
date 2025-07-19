#!/usr/bin/env python3
"""
Test script to verify User Modification validation logic
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_user_modification_validation():
    """Test the user modification validation logic"""
    print("🧪 Testing User Modification Validation Logic\n")
    
    # 1. Create two users
    print("1. Creating users...")
    user1_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john@example.com",
        "password": "password123"
    }
    
    user2_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com", 
        "password": "password123"
    }
    
    # Create user 1
    response = requests.post(f"{BASE_URL}/users/", json=user1_data)
    if response.status_code != 201:
        print(f"❌ Failed to create user 1: {response.text}")
        return
    user1_id = response.json()['id']
    
    # Create user 2
    response = requests.post(f"{BASE_URL}/users/", json=user2_data)
    if response.status_code != 201:
        print(f"❌ Failed to create user 2: {response.text}")
        return
    user2_id = response.json()['id']
    print(f"✅ Users created: {user1_id}, {user2_id}")
    
    # 2. Login as user 1
    print("\n2. Logging in as user 1...")
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Failed to login as user 1: {response.text}")
        return
    
    token1 = response.json()['access_token']
    headers1 = {"Authorization": f"Bearer {token1}"}
    print("✅ User 1 login successful")
    
    # 3. Login as user 2
    print("\n3. Logging in as user 2...")
    login_data2 = {
        "email": "jane@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data2)
    if response.status_code != 200:
        print(f"❌ Failed to login as user 2: {response.text}")
        return
    
    token2 = response.json()['access_token']
    headers2 = {"Authorization": f"Bearer {token2}"}
    print("✅ User 2 login successful")
    
    # 4. Test: User 1 updates their own profile (should succeed)
    print("\n4. Testing: User updating their own profile...")
    update_data = {
        "first_name": "Johnny",
        "last_name": "Updated"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=update_data, headers=headers1)
    if response.status_code == 200:
        print("✅ PASS: User can update their own profile")
    else:
        print(f"❌ FAIL: Expected 200 but got {response.status_code}: {response.text}")
    
    # 5. Test: User 1 tries to update user 2's profile (should fail with 403)
    print("\n5. Testing: User trying to update another user's profile...")
    update_data2 = {
        "first_name": "Hacker",
        "last_name": "Attempt"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user2_id}", json=update_data2, headers=headers1)
    if response.status_code == 403 and "Unauthorized action." in response.text:
        print("✅ PASS: User correctly blocked from updating another user's profile")
    else:
        print(f"❌ FAIL: Expected 403 with 'Unauthorized action.' but got {response.status_code}: {response.text}")
    
    # 6. Test: User tries to modify their email (should fail with 400)
    print("\n6. Testing: User trying to modify their email...")
    update_data3 = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "newemail@example.com"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=update_data3, headers=headers1)
    if response.status_code == 400 and "You cannot modify email or password." in response.text:
        print("✅ PASS: User correctly blocked from modifying email")
    else:
        print(f"❌ FAIL: Expected 400 with 'You cannot modify email or password.' but got {response.status_code}: {response.text}")
    
    # 7. Test: User tries to modify their password (should fail with 400)
    print("\n7. Testing: User trying to modify their password...")
    update_data4 = {
        "first_name": "John",
        "last_name": "Doe",
        "password": "newpassword123"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=update_data4, headers=headers1)
    if response.status_code == 400 and "You cannot modify email or password." in response.text:
        print("✅ PASS: User correctly blocked from modifying password")
    else:
        print(f"❌ FAIL: Expected 400 with 'You cannot modify email or password.' but got {response.status_code}: {response.text}")
    
    # 8. Test: User tries to modify both email and password (should fail with 400)
    print("\n8. Testing: User trying to modify both email and password...")
    update_data5 = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "anotheremail@example.com",
        "password": "anotherpassword123"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=update_data5, headers=headers1)
    if response.status_code == 400 and "You cannot modify email or password." in response.text:
        print("✅ PASS: User correctly blocked from modifying email and password")
    else:
        print(f"❌ FAIL: Expected 400 with 'You cannot modify email or password.' but got {response.status_code}: {response.text}")
    
    # 9. Test: Try to update non-existent user (should fail with 404)
    print("\n9. Testing: Updating non-existent user...")
    fake_user_id = "fake-user-id"
    response = requests.put(f"{BASE_URL}/users/{fake_user_id}", json=update_data, headers=headers1)
    if response.status_code == 404:
        print("✅ PASS: Non-existent user correctly returns 404")
    else:
        print(f"❌ FAIL: Expected 404 but got {response.status_code}: {response.text}")
    
    # 10. Test: Try to update without authentication (should fail with 401)
    print("\n10. Testing: Updating without authentication...")
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=update_data)
    if response.status_code == 401:
        print("✅ PASS: Unauthenticated request correctly returns 401")
    else:
        print(f"❌ FAIL: Expected 401 but got {response.status_code}: {response.text}")
    
    # 11. Test: Try to update with empty data (should fail with 400)
    print("\n11. Testing: Updating with empty data...")
    empty_data = {}
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=empty_data, headers=headers1)
    if response.status_code == 400:
        print("✅ PASS: Empty data correctly returns 400")
    else:
        print(f"❌ FAIL: Expected 400 but got {response.status_code}: {response.text}")
    
    # 12. Test: Try to update with invalid fields (should fail with 400)
    print("\n12. Testing: Updating with invalid fields...")
    invalid_data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "city": "New York"
    }
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=invalid_data, headers=headers1)
    if response.status_code == 400:
        print("✅ PASS: Invalid fields correctly returns 400")
    else:
        print(f"❌ FAIL: Expected 400 but got {response.status_code}: {response.text}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_user_modification_validation()
