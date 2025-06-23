#!/usr/bin/env python3
"""
Example demonstrating the GET /api/v1/reviews/ endpoint
This script shows how to retrieve all reviews from the API
"""

import requests
import json
import time
from app import create_app

def example_get_reviews():
    """Example showing how to use the GET /api/v1/reviews/ endpoint"""
    print("=== GET /api/v1/reviews/ Example ===\n")
    
    # Start the Flask app in test mode
    app = create_app()
    
    with app.test_client() as client:
        print("1. Testing GET /api/v1/reviews/ with empty database:")
        response = client.get('/api/v1/reviews/')
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
        print("\n2. Creating sample data...")
        
        # Create a user
        user_data = {
            "first_name": "Alice",
            "last_name": "Johnson", 
            "email": "alice.johnson@example.com"
        }
        user_response = client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        user_id = user_response.get_json()['id']
        print(f"   Created user: {user_id}")
        
        # Create an amenity
        amenity_data = {"name": "Pool"}
        amenity_response = client.post('/api/v1/amenities/',
                                     data=json.dumps(amenity_data),
                                     content_type='application/json')
        amenity_id = amenity_response.get_json()['id']
        print(f"   Created amenity: {amenity_id}")
        
        # Create a place
        place_data = {
            "title": "Beach House",
            "description": "Beautiful house by the beach",
            "price": 250.0,
            "latitude": 25.7617,
            "longitude": -80.1918,
            "owner_id": user_id,
            "amenities": [amenity_id]
        }
        place_response = client.post('/api/v1/places/',
                                   data=json.dumps(place_data),
                                   content_type='application/json')
        place_id = place_response.get_json()['id']
        print(f"   Created place: {place_id}")
        
        # Create multiple reviews
        reviews_data = [
            {
                "text": "Amazing beach house! Perfect for vacation.",
                "rating": 5,
                "user_id": user_id,
                "place_id": place_id
            },
            {
                "text": "Great location, but could use some updates.",
                "rating": 4,
                "user_id": user_id,
                "place_id": place_id
            },
            {
                "text": "Wonderful stay, highly recommend!",
                "rating": 5,
                "user_id": user_id,
                "place_id": place_id
            }
        ]
        
        for i, review_data in enumerate(reviews_data, 1):
            review_response = client.post('/api/v1/reviews/',
                                        data=json.dumps(review_data),
                                        content_type='application/json')
            review_id = review_response.get_json()['id']
            print(f"   Created review {i}: {review_id}")
        
        print("\n3. Retrieving all reviews:")
        response = client.get('/api/v1/reviews/')
        print(f"   Status: {response.status_code}")
        
        reviews = response.get_json()
        print(f"   Found {len(reviews)} reviews:")
        
        for i, review in enumerate(reviews, 1):
            print(f"\n   Review {i}:")
            print(f"     ID: {review['id']}")
            print(f"     Text: {review['text']}")
            print(f"     Rating: {review['rating']}/5")
            print(f"     User ID: {review['user_id']}")
            print(f"     Place ID: {review['place_id']}")
            print(f"     Created: {review['created_at']}")
            print(f"     Updated: {review['updated_at']}")
        
        print("\n4. Example using curl command:")
        print("   curl -X GET http://127.0.0.1:5000/api/v1/reviews/")
        
        print("\n5. Response format:")
        print("   The endpoint returns a JSON array of review objects.")
        print("   Each review object contains:")
        print("   - id: Unique review identifier")
        print("   - text: Review content/comment")
        print("   - rating: Rating value (1-5)")
        print("   - user_id: ID of the user who wrote the review")
        print("   - place_id: ID of the place being reviewed")
        print("   - created_at: Timestamp when review was created")
        print("   - updated_at: Timestamp when review was last updated")

if __name__ == "__main__":
    example_get_reviews()
