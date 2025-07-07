#!/usr/bin/env python3
"""
Test script for authentication flow
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_server_connection():
    """Test if the server is responding"""
    try:
        response = requests.get(f"{BASE_URL}/users", timeout=5)
        print(f"✓ Server is responding. Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Server connection failed: {e}")
        return False

def create_test_user():
    """Create a test user for authentication testing"""
    user_data = {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "password": "your_password"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users", json=user_data, timeout=5)
        print(f"User creation response: {response.status_code}")
        print(f"Response body: {response.text}")
        return response.status_code in [201, 400]  # 400 might mean user already exists
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to create user: {e}")
        return False

def test_login():
    """Test the login endpoint"""
    login_data = {
        "email": "john.doe@example.com",
        "password": "your_password"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=5)
        print(f"\n=== LOGIN TEST ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            if 'access_token' in token_data:
                print("✓ Login successful! JWT token received.")
                return token_data['access_token']
            else:
                print("✗ No access token in response")
                return None
        else:
            print("✗ Login failed")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Login request failed: {e}")
        return None

def test_protected_endpoint(token):
    """Test accessing a protected endpoint"""
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/protected", headers=headers, timeout=5)
        print(f"\n=== PROTECTED ENDPOINT TEST ===")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✓ Protected endpoint access successful!")
            return True
        else:
            print("✗ Protected endpoint access failed")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Protected endpoint request failed: {e}")
        return False

def main():
    print("Starting Authentication Flow Test...")
    
    # Test server connection
    if not test_server_connection():
        print("Please start the Flask server first: python3 run.py")
        return
    
    # Create test user
    print("\nCreating test user...")
    create_test_user()
    
    # Test login
    token = test_login()
    if not token:
        return
    
    # Test protected endpoint
    test_protected_endpoint(token)
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    main()
