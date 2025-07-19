#!/usr/bin/env python3
"""
Test script to verify Delete Review validation logic
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_delete_review_validation():
    """Test the delete review validation logic"""
    print("[TEST] Testing Delete Review Validation Logic\n")
    
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
        print(f"[FAIL] Failed to create user 1: {response.text}")
        return
    user1_id = response.json()['id']
    
    # Create user 2
    response = requests.post(f"{BASE_URL}/users/", json=user2_data)
    if response.status_code != 201:
        print(f"[FAIL] Failed to create user 2: {response.text}")
        return
    user2_id = response.json()['id']
    print(f"[SUCCESS] Users created: {user1_id}, {user2_id}")
    
    # 2. Login as user 1
    print("\n2. Logging in as user 1...")
    login_data = {
        "email": "john@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"[FAIL] Failed to login as user 1: {response.text}")
        return
    
    token1 = response.json()['access_token']
    headers1 = {"Authorization": f"Bearer {token1}"}
    print("[SUCCESS] User 1 login successful")
    
    # 3. Login as user 2
    print("\n3. Logging in as user 2...")
    login_data2 = {
        "email": "jane@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data2)
    if response.status_code != 200:
        print(f"[FAIL] Failed to login as user 2: {response.text}")
        return
    
    token2 = response.json()['access_token']
    headers2 = {"Authorization": f"Bearer {token2}"}
    print("[SUCCESS] User 2 login successful")
    
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
        print(f"[FAIL] Failed to create place: {response.text}")
        return
    
    place_id = response.json()['id']
    print(f"[SUCCESS] Place created with ID: {place_id}")
    
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
        print(f"[FAIL] Failed to create review: {response.text}")
        return
    
    review_id = response.json()['id']
    print(f"[SUCCESS] Review created with ID: {review_id}")
    
    # 6. Create another review as user 2 for deletion test
    print("\n6. Creating another review as user 2...")
    review_data2 = {
        "text": "Another great review!",
        "rating": 4,
        "user_id": user2_id,
        "place_id": place_id
    }
    
    # First, need to create another place for user 2 to review
    place_data2 = {
        "title": "Another Test Place",
        "description": "Another test place",
        "price": 150.0,
        "latitude": 41.8781,
        "longitude": -87.6298
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data2, headers=headers2)
    if response.status_code != 201:
        print(f"[FAIL] Failed to create second place: {response.text}")
        return
    
    place2_id = response.json()['id']
    
    # Now user 1 can review user 2's place
    review_data3 = {
        "text": "Nice place!",
        "rating": 4,
        "user_id": user1_id,
        "place_id": place2_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data3, headers=headers1)
    if response.status_code != 201:
        print(f"[FAIL] Failed to create second review: {response.text}")
        return
    
    review2_id = response.json()['id']
    print(f"[SUCCESS] Second review created with ID: {review2_id}")
    
    # 7. Test: User 1 (non-owner) tries to delete user 2's review (should fail with 403)
    print("\n7. Testing: Non-owner trying to delete review...")
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=headers1)
    if response.status_code == 403 and "Unauthorized action." in response.text:
        print("[PASS] Non-owner correctly blocked from deleting review")
    else:
        print(f"[FAIL] Expected 403 with 'Unauthorized action.' but got {response.status_code}: {response.text}")
    
    # 8. Test: User 2 (owner) deletes their own review (should succeed)
    print("\n8. Testing: Review owner deleting their own review...")
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=headers2)
    if response.status_code == 200:
        print("[PASS] Review owner can delete their own review")
    else:
        print(f"[FAIL] Expected 200 but got {response.status_code}: {response.text}")
    
    # 9. Test: Try to delete the same review again (should fail with 404)
    print("\n9. Testing: Deleting already deleted review...")
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=headers2)
    if response.status_code == 404:
        print("[PASS] Already deleted review correctly returns 404")
    else:
        print(f"[FAIL] Expected 404 but got {response.status_code}: {response.text}")
    
    # 10. Test: Try to delete non-existent review (should fail with 404)
    print("\n10. Testing: Deleting non-existent review...")
    fake_review_id = "fake-review-id"
    response = requests.delete(f"{BASE_URL}/reviews/{fake_review_id}", headers=headers1)
    if response.status_code == 404:
        print("[PASS] Non-existent review correctly returns 404")
    else:
        print(f"[FAIL] Expected 404 but got {response.status_code}: {response.text}")
    
    # 11. Test: Try to delete without authentication (should fail with 401)
    print("\n11. Testing: Deleting without authentication...")
    response = requests.delete(f"{BASE_URL}/reviews/{review2_id}")
    if response.status_code == 401:
        print("[PASS] Unauthenticated request correctly returns 401")
    else:
        print(f"[FAIL] Expected 401 but got {response.status_code}: {response.text}")
    
    # 12. Test: Clean up - User 1 deletes their own review
    print("\n12. Testing: Final cleanup - User 1 deletes their own review...")
    response = requests.delete(f"{BASE_URL}/reviews/{review2_id}", headers=headers1)
    if response.status_code == 200:
        print("[PASS] Final cleanup successful")
    else:
        print(f"[FAIL] Expected 200 but got {response.status_code}: {response.text}")
    
    print("\n[COMPLETE] All tests completed!")

if __name__ == "__main__":
    test_delete_review_validation()
