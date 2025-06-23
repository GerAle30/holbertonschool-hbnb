#!/usr/bin/env python3
"""Test script for the PUT /api/v1/users/<user_id> endpoint"""

import requests
import json

BASE_URL = "http://localhost:5001/api/v1/users/"

def create_test_user():
    """Create a test user first"""
    print("Step 1: Creating a test user...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    
    try:
        response = requests.post(BASE_URL, json=user_data, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            user = response.json()
            print(f"Created User: {json.dumps(user, indent=2)}")
            return user['id']
        else:
            print(f"Failed to create user: {response.text}")
            return None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def update_user(user_id):
    """Test updating the user"""
    print(f"\nStep 2: Updating user {user_id}...")
    
    # Update data
    update_data = {
        "first_name": "Jane",
        "last_name": "Smith", 
        "email": "jane.smith@example.com"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/users/{user_id}",
                                json=updated_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            updated_user = response.json()
            print(f"Updated User: {json.dumps(updated_user, indent=2)}")
            return True
        else:
            print(f"Failed to update user: {response.text}")
            return False
    except Exception as e:
        print(f"Error updating user: {e}")
        return False

def get_user(user_id):
    """Verify the user was updated"""
    print(f"\nStep 3: Verifying user {user_id} was updated...")
    
    try:
        response = requests.get(f"{BASE_URL}{user_id}", timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            print(f"Current User Data: {json.dumps(user, indent=2)}")
            return True
        else:
            print(f"Failed to get user: {response.text}")
            return False
    except Exception as e:
        print(f"Error getting user: {e}")
        return False

def test_update_nonexistent_user():
    """Test updating a non-existent user"""
    print(f"\nStep 4: Testing update on non-existent user...")
    
    fake_id = "fake-user-id-123"
    update_data = {
        "first_name": "Should",
        "last_name": "Fail",
        "email": "should.fail@example.com"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/users/{user_id}",
                                json=updated_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 404
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_duplicate_email_update(user_id):
    """Test updating to an email that already exists"""
    print(f"\nStep 5: Testing duplicate email update...")
    
    # First create another user
    print("Creating second user...")
    user_data = {
        "first_name": "Bob",
        "last_name": "Wilson",
        "email": "bob.wilson@example.com"
    }
    
    try:
        response = requests.post(BASE_URL, json=user_data, timeout=5)
        if response.status_code != 201:
            print("Failed to create second user for test")
            return False
        
        # Now try to update first user to use second user's email
        print("Attempting to update first user with duplicate email...")
        update_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "bob.wilson@example.com"  # This should fail
        }
        
        response = requests.put(f"{BASE_URL}/users/{user_id}",
                                json=duplicate_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing PUT /api/v1/users/<user_id> Endpoint ===\n")
    
    # Test the complete flow
    user_id = create_test_user()
    
    if user_id:
        # Test successful update
        update_success = update_user(user_id)
        
        if update_success:
            # Verify the update
            get_user(user_id)
            
            # Test error cases
            test_update_nonexistent_user()
            test_duplicate_email_update(user_id)
    
    print("\n=== PUT Endpoint Tests Completed ===")
