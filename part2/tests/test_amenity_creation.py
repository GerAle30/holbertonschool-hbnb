#!/usr/bin/env python3
"""
Test script for the amenity creation POST endpoint
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5000/api/v1"

def test_create_amenity():
    """Test creating a new amenity"""
    
    # Test data
    amenity_data = {
        "name": "Swimming Pool"
    }
    
    try:
        # Make POST request to create amenity
        response = requests.post(
            f"{BASE_URL}/amenities/",
            headers={"Content-Type": "application/json"},
            json=amenity_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("✅ Amenity created successfully!")
        else:
            print("❌ Failed to create amenity")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. "
              "Make sure the Flask app is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_create_amenity_invalid_data():
    """Test creating amenity with invalid data"""
    
    # Test with missing name
    invalid_data = {}
    
    try:
        response = requests.post(
            f"{BASE_URL}/amenities/",
            headers={"Content-Type": "application/json"},
            json=invalid_data
        )
        
        print(f"\nInvalid data test - Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("✅ Validation working correctly!")
        else:
            print("❌ Validation not working as expected")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. "
              "Make sure the Flask app is running.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Amenity Creation Endpoint")
    print("=" * 40)
    
    # Test valid amenity creation
    test_create_amenity()
    
    # Test invalid data handling
    test_create_amenity_invalid_data()
