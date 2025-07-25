#!/usr/bin/env python3
"""Basic functionality test"""

import requests
import json

BASE_URL = 'http://127.0.0.1:5001/api/v1'

def test_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    user_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{BASE_URL}/auth/register', json=user_data)
    print(f"Registration response: {response.status_code}")
    if response.status_code == 201:
        print("Registration successful")
    else:
        print(f"Registration failed: {response.text}")
    
    return response.status_code == 201

def test_login():
    """Test user login"""
    print("Testing user login...")
    
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login', json=login_data)
    print(f"Login response: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("Login successful")
        return token
    else:
        print(f"Login failed: {response.text}")
        return None

def test_users_endpoint(token):
    """Test users endpoint"""
    print("Testing users endpoint...")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f'{BASE_URL}/users/', headers=headers)
    
    print(f"Users endpoint response: {response.status_code}")
    if response.status_code == 200:
        users = response.json()
        print(f"Found {len(users)} users")
        return True
    else:
        print(f"Users endpoint failed: {response.text}")
        return False

def main():
    """Run basic tests"""
    print("Starting basic functionality tests...\n")
    
    # Test registration
    if test_registration():
        print()
        
        # Test login
        token = test_login()
        if token:
            print()
            
            # Test protected endpoint
            test_users_endpoint(token)
    
    print("\nBasic tests completed!")

if __name__ == '__main__':
    main()
