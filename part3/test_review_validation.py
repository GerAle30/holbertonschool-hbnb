#!/usr/bin/env python3
"""
Test script to verify Create Review validation logic
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_review_creation_validation():
    """Test the review creation validation logic"""
    print("🧪 Testing Create Review Validation Logic\n")
    
    # 1. First, create a user and get a token
    print("1. Creating a user...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code != 201:
        print(f"❌ Failed to create user: {response.text}")
        return
    
    user_id = response.json()['id']
    print(f"✅ User created with ID: {user_id}")
    
    # 2. Login to get JWT token
    print("\n2. Logging in...")
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Failed to login: {response.text}")
        return
    
    token = response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful, token obtained")
    
    # 3. Create a place owned by this user
    print("\n3. Creating a place...")
    place_data = {
        "title": "Test Place",
        "description": "A test place",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=headers)
    if response.status_code != 201:
        print(f"❌ Failed to create place: {response.text}")
        return
    
    place_id = response.json()['id']
    print(f"✅ Place created with ID: {place_id}")
    
    # 4. Create another user for testing
    print("\n4. Creating another user...")
    user2_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane@example.com", 
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user2_data)
    if response.status_code != 201:
        print(f"❌ Failed to create second user: {response.text}")
        return
    
    user2_id = response.json()['id']
    print(f"✅ Second user created with ID: {user2_id}")
    
    # 5. Login as second user
    print("\n5. Logging in as second user...")
    login2_data = {
        "email": "jane@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login2_data)
    if response.status_code != 200:
        print(f"❌ Failed to login as second user: {response.text}")
        return
    
    token2 = response.json()['access_token']
    headers2 = {"Authorization": f"Bearer {token2}"}
    print("✅ Second user login successful")
    
    # 6. Test: Try to review own place (should fail with 400)
    print("\n6. Testing: Owner trying to review own place...")
    review_data = {
        "text": "Great place!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=headers)
    if response.status_code == 400 and "You cannot review your own place." in response.text:
        print("✅ PASS: Owner correctly blocked from reviewing own place")
    else:
        print(f"❌ FAIL: Expected 400 with 'You cannot review your own place.' but got {response.status_code}: {response.text}")
    
    # 7. Test: Valid review by different user
    print("\n7. Testing: Valid review by different user...")
    review_data2 = {
        "text": "Great place!",
        "rating": 5,
        "user_id": user2_id,
        "place_id": place_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data2, headers=headers2)
    if response.status_code == 201:
        print("✅ PASS: Valid review created successfully")
        review_id = response.json()['id']
    else:
        print(f"❌ FAIL: Expected 201 but got {response.status_code}: {response.text}")
        return
    
    # 8. Test: Try to create duplicate review (should fail with 400)
    print("\n8. Testing: User trying to review same place twice...")
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data2, headers=headers2)
    if response.status_code == 400 and "You have already reviewed this place." in response.text:
        print("✅ PASS: Duplicate review correctly blocked")
    else:
        print(f"❌ FAIL: Expected 400 with 'You have already reviewed this place.' but got {response.status_code}: {response.text}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_review_creation_validation()
