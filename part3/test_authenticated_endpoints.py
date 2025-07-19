#!/usr/bin/env python3
"""
Comprehensive test script for authenticated endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/api/v1"

def print_separator(title):
    """Print a formatted separator for test sections"""
    print(f"\n{'='*60}")
    print(f"🔐 {title}")
    print(f"{'='*60}")

def print_test(test_name):
    """Print a formatted test name"""
    print(f"\n📋 {test_name}")
    print("-" * 50)

def test_authenticated_endpoints():
    """Test all authenticated endpoints with proper authorization"""
    
    print_separator("TESTING AUTHENTICATED ENDPOINTS")
    
    # Step 1: Create two users
    print_test("Step 1: Create Test Users")
    
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
    
    # Create User 1
    response = requests.post(f"{BASE_URL}/users/", json=user1_data)
    if response.status_code == 201:
        user1_id = response.json()['id']
        print(f"✅ User 1 created successfully: {user1_id}")
    else:
        print(f"❌ Failed to create User 1: {response.text}")
        return
    
    # Create User 2
    response = requests.post(f"{BASE_URL}/users/", json=user2_data)
    if response.status_code == 201:
        user2_id = response.json()['id']
        print(f"✅ User 2 created successfully: {user2_id}")
    else:
        print(f"❌ Failed to create User 2: {response.text}")
        return
    
    # Step 2: Login and get tokens
    print_test("Step 2: Login and Get JWT Tokens")
    
    # Login User 1
    login_data1 = {"email": "john@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data1)
    if response.status_code == 200:
        token1 = response.json()['access_token']
        headers1 = {"Authorization": f"Bearer {token1}", "Content-Type": "application/json"}
        print(f"✅ User 1 logged in successfully")
    else:
        print(f"❌ Failed to login User 1: {response.text}")
        return
    
    # Login User 2
    login_data2 = {"email": "jane@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data2)
    if response.status_code == 200:
        token2 = response.json()['access_token']
        headers2 = {"Authorization": f"Bearer {token2}", "Content-Type": "application/json"}
        print(f"✅ User 2 logged in successfully")
    else:
        print(f"❌ Failed to login User 2: {response.text}")
        return
    
    # Step 3: Test Place Creation (Authenticated)
    print_test("Step 3: Test Place Creation (Authenticated)")
    
    place_data = {
        "title": "John's Apartment",
        "description": "A cozy apartment in the city",
        "price": 100.0,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    
    # User 1 creates a place
    response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=headers1)
    if response.status_code == 201:
        place1_id = response.json()['id']
        print(f"✅ Place created successfully by User 1: {place1_id}")
        print(f"   Title: {response.json()['title']}")
        print(f"   Owner: {response.json()['owner']['first_name']} {response.json()['owner']['last_name']}")
    else:
        print(f"❌ Failed to create place: {response.text}")
        return
    
    # User 2 creates a place
    place_data2 = {
        "title": "Jane's House",
        "description": "A beautiful house by the beach",
        "price": 200.0,
        "latitude": 34.0522,
        "longitude": -118.2437
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data2, headers=headers2)
    if response.status_code == 201:
        place2_id = response.json()['id']
        print(f"✅ Place created successfully by User 2: {place2_id}")
    else:
        print(f"❌ Failed to create place for User 2: {response.text}")
        return
    
    # Step 4: Test Unauthorized Place Update
    print_test("Step 4: Test Unauthorized Place Update")
    
    # User 2 tries to update User 1's place (should fail)
    update_data = {
        "title": "HACKED PLACE",
        "description": "This should not work",
        "price": 999.0
    }
    
    response = requests.put(f"{BASE_URL}/places/{place1_id}", json=update_data, headers=headers2)
    if response.status_code == 403 and "Unauthorized action." in response.text:
        print(f"✅ Unauthorized place update correctly blocked")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json()['error']}")
    else:
        print(f"❌ Unauthorized place update not properly blocked: {response.text}")
    
    # Step 5: Test Authorized Place Update
    print_test("Step 5: Test Authorized Place Update")
    
    # User 1 updates their own place (should succeed)
    update_data = {
        "title": "John's Updated Apartment",
        "description": "An updated cozy apartment",
        "price": 120.0
    }
    
    response = requests.put(f"{BASE_URL}/places/{place1_id}", json=update_data, headers=headers1)
    if response.status_code == 200:
        print(f"✅ Authorized place update successful")
        print(f"   New title: {response.json()['title']}")
        print(f"   New price: ${response.json()['price']}")
    else:
        print(f"❌ Authorized place update failed: {response.text}")
    
    # Step 6: Test Review Creation
    print_test("Step 6: Test Review Creation")
    
    # User 2 reviews User 1's place (should succeed)
    review_data = {
        "text": "Great place to stay!",
        "rating": 5,
        "user_id": user2_id,
        "place_id": place1_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=headers2)
    if response.status_code == 201:
        review_id = response.json()['id']
        print(f"✅ Review created successfully: {review_id}")
        print(f"   Text: {response.json()['text']}")
        print(f"   Rating: {response.json()['rating']}")
    else:
        print(f"❌ Failed to create review: {response.text}")
        return
    
    # Step 7: Test Self-Review Prevention
    print_test("Step 7: Test Self-Review Prevention")
    
    # User 1 tries to review their own place (should fail)
    self_review_data = {
        "text": "My own place is great!",
        "rating": 5,
        "user_id": user1_id,
        "place_id": place1_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=self_review_data, headers=headers1)
    if response.status_code == 400 and "You cannot review your own place." in response.text:
        print(f"✅ Self-review correctly blocked")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json()['error']}")
    else:
        print(f"❌ Self-review not properly blocked: {response.text}")
    
    # Step 8: Test Duplicate Review Prevention
    print_test("Step 8: Test Duplicate Review Prevention")
    
    # User 2 tries to review the same place again (should fail)
    duplicate_review_data = {
        "text": "Another review for the same place",
        "rating": 4,
        "user_id": user2_id,
        "place_id": place1_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=duplicate_review_data, headers=headers2)
    if response.status_code == 400 and "You have already reviewed this place." in response.text:
        print(f"✅ Duplicate review correctly blocked")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json()['error']}")
    else:
        print(f"❌ Duplicate review not properly blocked: {response.text}")
    
    # Step 9: Test Unauthorized Review Update
    print_test("Step 9: Test Unauthorized Review Update")
    
    # User 1 tries to update User 2's review (should fail)
    review_update_data = {
        "text": "HACKED REVIEW",
        "rating": 1,
        "user_id": user2_id,
        "place_id": place1_id
    }
    
    response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=review_update_data, headers=headers1)
    if response.status_code == 403 and "Unauthorized action." in response.text:
        print(f"✅ Unauthorized review update correctly blocked")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json()['error']}")
    else:
        print(f"❌ Unauthorized review update not properly blocked: {response.text}")
    
    # Step 10: Test Authorized Review Update
    print_test("Step 10: Test Authorized Review Update")
    
    # User 2 updates their own review (should succeed)
    review_update_data = {
        "text": "Updated: Still a great place!",
        "rating": 4,
        "user_id": user2_id,
        "place_id": place1_id
    }
    
    response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=review_update_data, headers=headers2)
    if response.status_code == 200:
        print(f"✅ Authorized review update successful")
        print(f"   New text: {response.json()['text']}")
        print(f"   New rating: {response.json()['rating']}")
    else:
        print(f"❌ Authorized review update failed: {response.text}")
    
    # Step 11: Test Unauthorized Review Deletion
    print_test("Step 11: Test Unauthorized Review Deletion")
    
    # User 1 tries to delete User 2's review (should fail)
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=headers1)
    if response.status_code == 403 and "Unauthorized action." in response.text:
        print(f"✅ Unauthorized review deletion correctly blocked")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json()['error']}")
    else:
        print(f"❌ Unauthorized review deletion not properly blocked: {response.text}")
    
    # Step 12: Test User Profile Updates
    print_test("Step 12: Test User Profile Updates")
    
    # User 1 updates their own profile (should succeed)
    profile_update_data = {
        "first_name": "Johnny",
        "last_name": "Updated"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=profile_update_data, headers=headers1)
    if response.status_code == 200:
        print(f"✅ User profile update successful")
        print(f"   New name: {response.json()['first_name']} {response.json()['last_name']}")
    else:
        print(f"❌ User profile update failed: {response.text}")
    
    # Step 13: Test Unauthorized User Profile Update
    print_test("Step 13: Test Unauthorized User Profile Update")
    
    # User 2 tries to update User 1's profile (should fail)
    hack_profile_data = {
        "first_name": "HACKED",
        "last_name": "USER"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=hack_profile_data, headers=headers2)
    if response.status_code == 403 and "Unauthorized action." in response.text:
        print(f"✅ Unauthorized user profile update correctly blocked")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json()['error']}")
    else:
        print(f"❌ Unauthorized user profile update not properly blocked: {response.text}")
    
    # Step 14: Test Email/Password Update Prevention
    print_test("Step 14: Test Email/Password Update Prevention")
    
    # User 1 tries to update their email (should fail)
    email_update_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "newemail@example.com"
    }
    
    response = requests.put(f"{BASE_URL}/users/{user1_id}", json=email_update_data, headers=headers1)
    if response.status_code == 400 and "You cannot modify email or password." in response.text:
        print(f"✅ Email update correctly blocked")
        print(f"   Status: {response.status_code}")
        print(f"   Message: {response.json()['error']}")
    else:
        print(f"❌ Email update not properly blocked: {response.text}")
    
    # Step 15: Test No Authentication
    print_test("Step 15: Test No Authentication")
    
    # Try to create a place without authentication (should fail)
    response = requests.post(f"{BASE_URL}/places/", json=place_data)
    if response.status_code == 401:
        print(f"✅ Unauthenticated place creation correctly blocked")
        print(f"   Status: {response.status_code}")
    else:
        print(f"❌ Unauthenticated place creation not properly blocked: {response.text}")
    
    # Clean up: Delete the review for final test
    print_test("Step 16: Test Authorized Review Deletion")
    
    # User 2 deletes their own review (should succeed)
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=headers2)
    if response.status_code == 200:
        print(f"✅ Authorized review deletion successful")
        print(f"   Message: {response.json()['message']}")
    else:
        print(f"❌ Authorized review deletion failed: {response.text}")
    
    print_separator("ALL TESTS COMPLETED")
    print(f"✅ Authentication and authorization tests finished!")
    print(f"🔒 All protected endpoints are working correctly!")

if __name__ == "__main__":
    test_authenticated_endpoints()
