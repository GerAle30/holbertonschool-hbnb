#!/usr/bin/env python3
"""
Test script to verify public endpoints work without authentication
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_public_endpoint(method, endpoint, data=None):
    """Test a public endpoint without authentication"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=5)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, timeout=5)
        elif method.upper() == 'PUT':
            response = requests.put(url, json=data, timeout=5)
        else:
            print(f"[ERROR] Unsupported method: {method}")
            return False
            
        print(f"[SUCCESS] {method.upper()} {endpoint}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        print()
        
        return response.status_code in [200, 201]
        
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] {method.upper()} {endpoint} - Failed: {e}")
        return False

def test_protected_endpoint_without_auth(method, endpoint):
    """Test that protected endpoints return 401 without authentication"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=5)
        elif method.upper() == 'POST':
            response = requests.post(url, json={}, timeout=5)
        elif method.upper() == 'PUT':
            response = requests.put(url, json={}, timeout=5)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, timeout=5)
        else:
            print(f"[ERROR] Unsupported method: {method}")
            return False
            
        print(f"[PROTECTED] {method.upper()} {endpoint}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:100]}...")
        print()
        
        return response.status_code == 401
        
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] {method.upper()} {endpoint} - Failed: {e}")
        return False

def main():
    print("=" * 60)
    print("TESTING PUBLIC ENDPOINTS (No Authentication Required)")
    print("=" * 60)
    
    # Test the two endpoints specifically mentioned as public
    public_endpoints = [
        ("GET", "/places/"),
        ("GET", "/places/dummy-id"),  # Should return 404 but not 401
    ]
    
    for method, endpoint in public_endpoints:
        test_public_endpoint(method, endpoint)
    
    print("=" * 60)
    print("TESTING OTHER PUBLIC ENDPOINTS")
    print("=" * 60)
    
    # Test other endpoints that should be public
    other_public_endpoints = [
        ("GET", "/users/"),
        ("GET", "/users/dummy-id"),
        ("POST", "/users/", {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "testpass"
        }),
        ("GET", "/reviews/"),
        ("GET", "/reviews/dummy-id"),
        ("GET", "/amenities/"),
        ("GET", "/amenities/dummy-id"),
        ("POST", "/auth/login", {
            "email": "test@example.com",
            "password": "wrong_password"
        }),
    ]
    
    for method, endpoint, *data in other_public_endpoints:
        payload = data[0] if data else None
        test_public_endpoint(method, endpoint, payload)
    
    print("=" * 60)
    print("TESTING PROTECTED ENDPOINTS (Should Return 401)")
    print("=" * 60)
    
    # Test endpoints that should require authentication
    protected_endpoints = [
        ("POST", "/places/"),
        ("PUT", "/places/dummy-id"),
        ("POST", "/reviews/"),
        ("PUT", "/reviews/dummy-id"),
        ("DELETE", "/reviews/dummy-id"),
        ("PUT", "/users/dummy-id"),
        ("GET", "/auth/protected"),
    ]
    
    for method, endpoint in protected_endpoints:
        test_protected_endpoint_without_auth(method, endpoint)
    
    print("=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    main()
