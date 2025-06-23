#!/usr/bin/env python3

import json
import requests
import time
import subprocess
import sys
from threading import Thread

def start_server():
    """Start the Flask server in a separate process"""
    from app import create_app
    app = create_app()
    app.run(debug=False, port=5003, use_reloader=False)

def test_place_registration():
    """Test the place registration endpoint"""
    base_url = "http://localhost:5003/api/v1"
    
    # Wait for server to be ready
    print("Waiting for server to start...")
    for i in range(10):
        try:
            response = requests.get(f"{base_url}/users/", timeout=2)
            print("Server is ready!")
            break
        except:
            time.sleep(1)
    else:
        print("Server failed to start")
        return
    
    try:
        # First, create a user to be the owner
        print("\n1. Creating a user (owner)...")
        user_data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com"
        }
        
        response = requests.post(f"{base_url}/users/", json=user_data)
        print(f"User creation response: {response.status_code}")
        if response.status_code == 201:
            user = response.json()
            owner_id = user['id']
            print(f"Created user with ID: {owner_id}")
        else:
            print(f"Failed to create user: {response.text}")
            return
        
        # Create some amenities
        print("\n2. Creating amenities...")
        amenities = []
        for amenity_name in ["WiFi", "Pool", "Parking"]:
            amenity_data = {"name": amenity_name}
            response = requests.post(f"{base_url}/amenities/",
                                     json=amenity_data)
            if response.status_code == 201:
                amenity = response.json()
                amenities.append(amenity['id'])
                print(f"   Created amenity '{amenity_name}' with "
                      f"ID: {amenity['id']}")
        
        # Now create a place
        print("\n3. Creating a place...")
        place_data = {
            "title": "Beautiful Beach House",
            "description": "A lovely house by the beach with "
                          "stunning ocean views",
            "price": 150.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": owner_id,
            "amenities": amenities[:2]  # Use first 2 amenities
        }
        
        response = requests.post(f"{base_url}/places/", json=place_data)
        print(f"Place creation response: {response.status_code}")
        
        if response.status_code == 201:
            place = response.json()
            print("✅ SUCCESS! Place created successfully:")
            print(json.dumps(place, indent=2))
        else:
            print(f"❌ FAILED to create place: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    # Start server in a thread
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run the test
    test_place_registration()
