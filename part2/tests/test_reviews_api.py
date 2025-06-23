#!/usr/bin/env python3
"""Test script for the GET /api/v1/reviews/ endpoint"""

from app import create_app
import json

def test_get_all_reviews():
    """Test the GET /api/v1/reviews/ endpoint"""
    app = create_app()
    
    with app.test_client() as client:
        # Test GET /api/v1/reviews/ with empty repository
        response = client.get('/api/v1/reviews/')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.get_json()}")
        print(f"Expected: Empty list since no reviews exist yet")
        
        # Now let's create some test data and test again
        # First create a user
        user_data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com"
        }
        user_response = client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        print(f"\nUser created: {user_response.get_json()}")
        user_id = user_response.get_json()['id']
        
        # Create an amenity
        amenity_data = {"name": "WiFi"}
        amenity_response = client.post('/api/v1/amenities/',
                                     data=json.dumps(amenity_data),
                                     content_type='application/json')
        print(f"Amenity created: {amenity_response.get_json()}")
        amenity_id = amenity_response.get_json()['id']
        
        # Create a place
        place_data = {
            "title": "Lovely Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": user_id,
            "amenities": [amenity_id]
        }
        place_response = client.post('/api/v1/places/',
                                   data=json.dumps(place_data),
                                   content_type='application/json')
        print(f"Place created: {place_response.get_json()}")
        place_id = place_response.get_json()['id']
        
        # Create a review
        review_data = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        review_response = client.post('/api/v1/reviews/',
                                    data=json.dumps(review_data),
                                    content_type='application/json')
        print(f"Review created: {review_response.get_json()}")
        
        # Test GET /api/v1/reviews/ again - now should have one review
        response = client.get('/api/v1/reviews/')
        print(f"\nAfter creating review:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.get_json(), indent=2)}")
        
        # Verify the response structure
        reviews = response.get_json()
        if reviews and len(reviews) > 0:
            review = reviews[0]
            expected_fields = ['id', 'text', 'rating', 'user_id',
                               'place_id', 'created_at', 'updated_at']
            print(f"\nReview fields: {list(review.keys())}")
            print(f"Expected fields: {expected_fields}")
            print(f"All fields present: "
                  f"{all(field in review for field in expected_fields)}")

if __name__ == "__main__":
    test_get_all_reviews()
