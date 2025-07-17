#!/usr/bin/env python3
"""
Test script to verify Update Review validation logic
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_update_review_validation():
    """Test the update review validation logic"""
    print("🧪 Testing Update Review Validation Logic\n")
    
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
    
    # 4. Create a place as user 1
    print("\n4. Creating a place as user 1...")
    place_data = {
        "title": "Test Place",
        "description": "A test place",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=headers1)
    if response.status_code != 201:
        print(f"❌ Failed to create place: {response.text}")
        return
    
    place_id = response.json()['id']
    print(f"✅ Place created with ID: {place_id}")
    
    # 5. Create a review as user 2 (user 2 reviews user 1's place)
    print("\n5. Creating a review as user 2...")
    review_data = {
        "text": "Great place!",
        "rating": 5,
        "user_id": user2_id,
        "place_id": place_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=headers2)
    if response.status_code != 201:
        print(f"❌ Failed to create review: {response.text}")
        return
    
    review_id = response.json()['id']
    print(f"✅ Review created with ID: {review_id}")
    
    # 6. Test: User 2 (owner) updates their own review (should succeed)
    print("\n6. Testing: Review owner updating their own review...")
    update_data = {
        "text": "Updated review text",
        "rating": 4,
        "user_id": user2_id,
        "place_id": place_id
    }
    
    response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data, headers=headers2)
    if response.status_code == 200:
        print("✅ PASS: Review owner can update their own review")
    else:
        print(f"❌ FAIL: Expected 200 but got {response.status_code}: {response.text}")
    
    # 7. Test: User 1 (non-owner) tries to update user 2's review (should fail with 403)
    print("\n7. Testing: Non-owner trying to update review...")
    update_data2 = {
        "text": "Trying to update someone else's review",
        "rating": 1,
        "user_id": user2_id,
        "place_id": place_id
    }
    
    response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data2, headers=headers1)
    if response.status_code == 403 and "Unauthorized action." in response.text:
        print("✅ PASS: Non-owner correctly blocked from updating review")
    else:
        print(f"❌ FAIL: Expected 403 with 'Unauthorized action.' but got {response.status_code}: {response.text}")
    
    # 8. Test: Try to update non-existent review (should fail with 404)
    print("\n8. Testing: Updating non-existent review...")
    fake_review_id = "fake-review-id"
    response = requests.put(f"{BASE_URL}/reviews/{fake_review_id}", json=update_data, headers=headers2)
    if response.status_code == 404:
        print("✅ PASS: Non-existent review correctly returns 404")
    else:
        print(f"❌ FAIL: Expected 404 but got {response.status_code}: {response.text}")
    
    # 9. Test: Try to update without authentication (should fail with 401)
    print("\n9. Testing: Updating without authentication...")
    response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data)
    if response.status_code == 401:
        print("✅ PASS: Unauthenticated request correctly returns 401")
    else:
        print(f"❌ FAIL: Expected 401 but got {response.status_code}: {response.text}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_update_review_validation()
