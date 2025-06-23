#!/usr/bin/env python3
"""Example usage of the review registration API endpoint."""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:5001/api/v1"

def create_sample_data():
    """Create sample user, amenity, and place for testing."""
    print("Creating sample data...")
    
    # Create a user
    user_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    }
    
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    if response.status_code == 201:
        user = response.json()
        print(f"✅ User created: {user['id']}")
    else:
        print(f"❌ Failed to create user: {response.status_code}")
        return None, None
    
    # Create an amenity
    amenity_data = {"name": "Swimming Pool"}
    response = requests.post(f"{BASE_URL}/amenities/", json=amenity_data)
    if response.status_code == 201:
        amenity = response.json()
        print(f"✅ Amenity created: {amenity['id']}")
    else:
        print(f"❌ Failed to create amenity: {response.status_code}")
        return user, None
    
    # Create a place
    place_data = {
        "title": "Luxury Villa",
        "description": "Beautiful villa with ocean view",
        "price": 250.0,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "owner_id": user["id"],
        "amenities": [amenity["id"]]
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data)
    if response.status_code == 201:
        place = response.json()
        print(f"✅ Place created: {place['id']}")
        return user, place
    else:
        print(f"❌ Failed to create place: {response.status_code}")
        return user, None

def create_review(user_id, place_id):
    """Create a review using the API endpoint."""
    print("\\nCreating review...")
    
    review_data = {
        "text": "Amazing place! The ocean view was breathtaking and "
                "the pool was perfect.",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=review_data)
    
    if response.status_code == 201:
        review = response.json()
        print(f"✅ Review created successfully!")
        print(f"   Review ID: {review['id']}")
        print(f"   Rating: {review['rating']}/5")
        print(f"   Text: {review['text']}")
        print(f"   Created at: {review['created_at']}")
        return review
    else:
        print(f"❌ Failed to create review: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data}")
        except:
            print(f"   Raw response: {response.text}")
        return None

def test_invalid_review():
    """Test creating a review with invalid data."""
    print("\\nTesting invalid review data...")
    
    # Test with invalid rating
    invalid_review_data = {
        "text": "Test review",
        "rating": 10,  # Invalid rating (should be 1-5)
        "user_id": "invalid-user-id",
        "place_id": "invalid-place-id"
    }
    
    response = requests.post(f"{BASE_URL}/reviews/", json=invalid_review_data)
    
    if response.status_code == 400:
        print("✅ Correctly rejected invalid review data")
        error_data = response.json()
        print(f"   Error message: {error_data.get('error', 'Unknown error')}")
    else:
        print(f"❌ Unexpected response: {response.status_code}")

def main():
    """Main function to demonstrate the review API."""
    print("🚀 Testing Review Registration API (POST /api/v1/reviews/)\\n")
    
    try:
        # Create sample data
        user, place = create_sample_data()
        
        if user and place:
            # Create a review
            review = create_review(user["id"], place["id"])
            
            if review:
                print("\\n✅ Review API is working correctly!")
        
        # Test invalid data
        test_invalid_review()
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server.")
        print("   Make sure the server is running on http://localhost:5001")
        print("   Run: python run.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
