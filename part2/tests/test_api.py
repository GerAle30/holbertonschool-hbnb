#!/usr/bin/env python3
"""Test script for the User API endpoints"""

import requests
import json
import sys

BASE_URL = "http://localhost:5001/api/v1/users/"

def test_get_empty_users():
    """Test GET /api/v1/users/ when no users exist"""
    print("Testing GET /api/v1/users/ (empty list)...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.Timeout:
        print("Request timed out!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_user():
    """Test POST /api/v1/users/ to create a new user"""
    print("\nTesting POST /api/v1/users/ (create user)...")
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com"
    }
    
    try:
        response = requests.post(BASE_URL, 
                               json=user_data, 
                               headers={"Content-Type": "application/json"},
                               timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.json() if response.status_code == 201 else None
    except requests.exceptions.Timeout:
        print("Request timed out!")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_get_users_with_data():
    """Test GET /api/v1/users/ when users exist"""
    print("\nTesting GET /api/v1/users/ (with data)...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.Timeout:
        print("Request timed out!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_user_by_id(user_id):
    """Test GET /api/v1/users/<user_id>"""
    print(f"\nTesting GET /api/v1/users/{user_id}...")
    try:
        response = requests.get(f"{BASE_URL}{user_id}", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.Timeout:
        print("Request timed out!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing User API Endpoints ===\n")
    
    # Test 1: Get empty users list
    test_get_empty_users()
    
    # Test 2: Create a user
    created_user = test_create_user()
    
    # Test 3: Get users list (should have 1 user now)
    test_get_users_with_data()
    
    # Test 4: Get user by ID (if user was created successfully)
    if created_user and 'id' in created_user:
        test_get_user_by_id(created_user['id'])
    
    print("\n=== Tests Completed ===")
