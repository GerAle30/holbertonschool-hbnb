#!/usr/bin/env python3
"""
Comprehensive Entity Testing Script for HBnB Project
Tests all CRUD operations for User, Place, Amenity, and Review entities
"""
import requests
import json
import sys

BASE_URL = "http://localhost:5555/api/v1"

def get_admin_token():
    """Login as admin and get JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login", 
        json={
            "email": "admin@test.com",
            "password": "admin123"
        })
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to login as admin: {response.text}")
        return None

def get_user_token():
    """Login as regular user and get JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login",
        json={
            "email": "john@test.com", 
            "password": "user123"
        })
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Failed to login as regular user: {response.text}")
        return None

def test_users(admin_token):
    """Test User CRUD operations"""
    print("\n=== TESTING USER ENTITY ===")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # GET all users
    print("1. Testing GET all users...")
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    print(f"   Status: {response.status_code}")
    users = response.json()
    print(f"   Found {len(users)} users")
    
    # CREATE a new user
    print("2. Testing CREATE user...")
    new_user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "password123",
        "is_admin": False
    }
    response = requests.post(f"{BASE_URL}/users/", json=new_user_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        new_user = response.json()
        user_id = new_user["id"]
        print(f"   Created user with ID: {user_id}")
        
        # GET specific user
        print("3. Testing GET specific user...")
        response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        
        # UPDATE user
        print("4. Testing UPDATE user...")
        update_data = {"first_name": "Updated", "last_name": "Name"}
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        return user_id
    else:
        print(f"   Failed to create user: {response.text}")
        return None

def test_amenities(admin_token):
    """Test Amenity CRUD operations"""
    print("\n=== TESTING AMENITY ENTITY ===")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # GET all amenities
    print("1. Testing GET all amenities...")
    response = requests.get(f"{BASE_URL}/amenities/", headers=headers)
    print(f"   Status: {response.status_code}")
    amenities = response.json()
    print(f"   Found {len(amenities)} amenities")
    
    # CREATE a new amenity
    print("2. Testing CREATE amenity...")
    new_amenity_data = {"name": "Test Amenity"}
    response = requests.post(f"{BASE_URL}/amenities/", json=new_amenity_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        new_amenity = response.json()
        amenity_id = new_amenity["id"]
        print(f"   Created amenity with ID: {amenity_id}")
        
        # GET specific amenity
        print("3. Testing GET specific amenity...")
        response = requests.get(f"{BASE_URL}/amenities/{amenity_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        
        # UPDATE amenity
        print("4. Testing UPDATE amenity...")
        update_data = {"name": "Updated Test Amenity"}
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json=update_data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        return amenity_id
    else:
        print(f"   Failed to create amenity: {response.text}")
        return None

def test_places(admin_token):
    """Test Place CRUD operations"""
    print("\n=== TESTING PLACE ENTITY ===")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # GET all places
    print("1. Testing GET all places...")
    response = requests.get(f"{BASE_URL}/places/", headers=headers)
    print(f"   Status: {response.status_code}")
    places = response.json()
    print(f"   Found {len(places)} places")
    
    # CREATE a new place
    print("2. Testing CREATE place...")
    new_place_data = {
        "title": "Test Place",
        "description": "A test place for comprehensive testing",
        "price": 150.00,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "amenities": []
    }
    response = requests.post(f"{BASE_URL}/places/", json=new_place_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        new_place = response.json()
        place_id = new_place["id"]
        print(f"   Created place with ID: {place_id}")
        
        # GET specific place
        print("3. Testing GET specific place...")
        response = requests.get(f"{BASE_URL}/places/{place_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        
        # UPDATE place
        print("4. Testing UPDATE place...")
        update_data = {"title": "Updated Test Place", "price": 200.00}
        response = requests.put(f"{BASE_URL}/places/{place_id}", json=update_data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        return place_id
    else:
        print(f"   Failed to create place: {response.text}")
        return None

def test_reviews(user_token, place_id, user_id):
    """Test Review CRUD operations"""
    print("\n=== TESTING REVIEW ENTITY ===")
    headers = {"Authorization": f"Bearer {user_token}"}
    
    if not place_id or not user_id:
        print("   Skipping review tests - missing place_id or user_id")
        return None
        
    # GET all reviews
    print("1. Testing GET all reviews...")
    response = requests.get(f"{BASE_URL}/reviews/", headers=headers)
    print(f"   Status: {response.status_code}")
    reviews = response.json()
    print(f"   Found {len(reviews)} reviews")
    
    # CREATE a new review
    print("2. Testing CREATE review...")
    new_review_data = {
        "text": "This is a comprehensive test review",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    response = requests.post(f"{BASE_URL}/reviews/", json=new_review_data, headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        new_review = response.json()
        review_id = new_review["id"]
        print(f"   Created review with ID: {review_id}")
        
        # GET specific review
        print("3. Testing GET specific review...")
        response = requests.get(f"{BASE_URL}/reviews/{review_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        
        # UPDATE review
        print("4. Testing UPDATE review...")
        update_data = {"text": "Updated comprehensive test review", "rating": 4}
        response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=update_data, headers=headers)
        print(f"   Status: {response.status_code}")
        
        # DELETE review
        print("5. Testing DELETE review...")
        response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=headers)
        print(f"   Status: {response.status_code}")
        
        return review_id
    else:
        print(f"   Failed to create review: {response.text}")
        return None

def main():
    """Run comprehensive tests for all entities"""
    print("Starting Comprehensive Entity Testing...")
    print("=" * 50)
    
    # Get tokens
    admin_token = get_admin_token()
    user_token = get_user_token()
    
    if not admin_token:
        print("Failed to get admin token. Exiting.")
        sys.exit(1)
        
    if not user_token:
        print("Failed to get user token. Exiting.")
        sys.exit(1)
    
    # Test all entities
    user_id = test_users(admin_token)
    amenity_id = test_amenities(admin_token)
    place_id = test_places(admin_token)
    review_id = test_reviews(user_token, place_id, "d99d76a4-9756-44e9-9504-f4aadec10553")  # John's user ID
    
    print("\n" + "=" * 50)
    print("COMPREHENSIVE TESTING COMPLETED!")
    print("=" * 50)
    
    # Summary
    print(f"\nSUMMARY:")
    print(f"- User operations: {'✓' if user_id else '✗'}")
    print(f"- Amenity operations: {'✓' if amenity_id else '✗'}")
    print(f"- Place operations: {'✓' if place_id else '✗'}")
    print(f"- Review operations: {'✓' if review_id else '✗'}")
    
if __name__ == "__main__":
    main()
