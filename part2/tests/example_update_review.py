#!/usr/bin/env python3
"""
Example demonstrating the PUT /api/v1/reviews/<review_id> endpoint
This script shows how to update review information via the API
"""

from app import create_app
import json

def example_update_review():
    """Example showing how to use the PUT /api/v1/reviews/<review_id> API."""
    print("=== PUT /api/v1/reviews/<review_id> Example ===\n")
    
    app = create_app()
    
    with app.test_client() as client:
        print("1. Setting up test data...")
        
        # Create a user
        user_data = {
            "first_name": "Sarah",
            "last_name": "Connor", 
            "email": "sarah.connor@example.com"
        }
        user_response = client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        user_id = user_response.get_json()['id']
        print(f"   Created user: {user_id}")
        
        # Create an amenity
        amenity_data = {"name": "WiFi"}
        amenity_response = client.post('/api/v1/amenities/',
                                     data=json.dumps(amenity_data),
                                     content_type='application/json')
        amenity_id = amenity_response.get_json()['id']
        
        # Create a place
        place_data = {
            "title": "Mountain Cabin",
            "description": "A peaceful cabin in the mountains",
            "price": 180.0,
            "latitude": 45.5017,
            "longitude": -73.5673,
            "owner_id": user_id,
            "amenities": [amenity_id]
        }
        place_response = client.post('/api/v1/places/',
                                   data=json.dumps(place_data),
                                   content_type='application/json')
        place_id = place_response.get_json()['id']
        
        # Create a review
        initial_review_data = {
            "text": "The cabin was okay, nothing special.",
            "rating": 2,
            "user_id": user_id,
            "place_id": place_id
        }
        review_response = client.post('/api/v1/reviews/',
                                    data=json.dumps(initial_review_data),
                                    content_type='application/json')
        review_id = review_response.get_json()['id']
        print(f"   Created initial review: {review_id}")
        
        print("\n2. Original review:")
        original_review = review_response.get_json()
        print(f"   Text: '{original_review['text']}'")
        print(f"   Rating: {original_review['rating']}/5")
        print(f"   Created: {original_review['created_at']}")
        print(f"   Updated: {original_review['updated_at']}")
        
        # Update just the text and rating
        print("\n3. Updating review text and rating...")
        update_data = {
            "text": "Actually, after thinking about it more, the cabin "
                    "was wonderful! Very peaceful and exactly what I needed.",
            "rating": 5
        }
        
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        if response.status_code == 200:
            updated_review = response.get_json()
            print(f"   ✅ Update successful!")
            print(f"   New text: '{updated_review['text']}'")
            print(f"   New rating: {updated_review['rating']}/5")
            print(f"   Updated timestamp: {updated_review['updated_at']}")
            print(f"   (Original created timestamp preserved: "
                  f"{updated_review['created_at']})")
        else:
            print(f"   ❌ Update failed: {response.get_json()}")
        
        print("\n4. Demonstrating field-specific updates...")
        
        # Update only rating
        print("   Updating only the rating...")
        rating_update = {"rating": 4}
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(rating_update),
                            content_type='application/json')
        if response.status_code == 200:
            review = response.get_json()
            print(f"   New rating: {review['rating']}/5")
            print(f"   Text unchanged: '{review['text'][:50]}...'")
        
        # Update only text
        print("   Updating only the text...")
        text_update = {"text": "Final review: This mountain cabin "
                               "exceeded all expectations!"}
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(text_update),
                            content_type='application/json')
        if response.status_code == 200:
            review = response.get_json()
            print(f"   New text: '{review['text']}'")
            print(f"   Rating unchanged: {review['rating']}/5")
        
        print("\n5. Demonstrating error handling...")
        
        # Try to update with invalid rating
        print("   Testing invalid rating (out of range)...")
        invalid_data = {"rating": 6}
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(invalid_data),
                            content_type='application/json')
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.get_json()['error']}")
        
        # Try to update non-existent review
        print("   Testing non-existent review...")
        response = client.put('/api/v1/reviews/fake-review-id',
                            data=json.dumps({"text": "Test"}),
                            content_type='application/json')
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.get_json()['error']}")
        
        print("\n6. API Usage Summary:")
        print("   Endpoint: PUT /api/v1/reviews/<review_id>")
        print("   Purpose: Update review information")
        print("   Content-Type: application/json")
        print("   ")
        print("   Updatable fields:")
        print("   - text: Review content/comment")
        print("   - rating: Rating value (1-5)")
        print("   - user_id: ID of the user (validates existence)")
        print("   - place_id: ID of the place (validates existence)")
        print("   ")
        print("   Response codes:")
        print("   - 200: Success (returns updated review)")
        print("   - 400: Invalid input data")
        print("   - 404: Review not found")
        print("   ")
        print("   curl example:")
        print(f'   curl -X PUT http://127.0.0.1:5000/api/v1/reviews/'
        print('        -H "Content-Type: application/json" \\')
        print('        -d \'{"text": "Updated review text", "rating": 5}\'')

if __name__ == "__main__":
    example_update_review()
