#!/usr/bin/env python3
"""Test script for the PUT /api/v1/reviews/<review_id> endpoint"""

from app import create_app
import json

def test_update_review():
    """Test the PUT /api/v1/reviews/<review_id> endpoint"""
    app = create_app()
    
    with app.test_client() as client:
        print("=== PUT /api/v1/reviews/<review_id> Test ===\n")
        
        # Step 1: Create test data
        print("1. Creating test data...")
        
        # Create a user
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith", 
            "email": "jane.smith@example.com"
        }
        user_response = client.post('/api/v1/users/', 
                                  data=json.dumps(user_data),
                                  content_type='application/json')
        user_id = user_response.get_json()['id']
        print(f"   Created user: {user_id}")
        
        # Create an amenity
        amenity_data = {"name": "Gym"}
        amenity_response = client.post('/api/v1/amenities/',
                                     data=json.dumps(amenity_data),
                                     content_type='application/json')
        amenity_id = amenity_response.get_json()['id']
        print(f"   Created amenity: {amenity_id}")
        
        # Create a place
        place_data = {
            "title": "Modern Apartment",
            "description": "A modern apartment in the city center",
            "price": 150.0,
            "latitude": 40.7589,
            "longitude": -73.9851,
            "owner_id": user_id,
            "amenities": [amenity_id]
        }
        place_response = client.post('/api/v1/places/',
                                   data=json.dumps(place_data),
                                   content_type='application/json')
        place_id = place_response.get_json()['id']
        print(f"   Created place: {place_id}")
        
        # Create a review
        review_data = {
            "text": "Nice place, but could be cleaner.",
            "rating": 3,
            "user_id": user_id,
            "place_id": place_id
        }
        review_response = client.post('/api/v1/reviews/',
                                    data=json.dumps(review_data),
                                    content_type='application/json')
        review_id = review_response.get_json()['id']
        print(f"   Created review: {review_id}")
        print(f"   Original review: "
              f"{json.dumps(review_response.get_json(), indent=4)}")
        
        # Step 2: Test successful update (partial update)
        print("\n2. Testing successful partial update...")
        update_data = {
            "text": "Actually, the place was great! "
                    "Very clean and comfortable.",
            "rating": 5
        }
        
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        print(f"   Status Code: {response.status_code}")
        updated_review = response.get_json()
        print(f"   Updated review: {json.dumps(updated_review, indent=4)}")
        
        # Verify changes
        assert response.status_code == 200
        assert updated_review['text'] == update_data['text']
        assert updated_review['rating'] == update_data['rating']
        assert updated_review['user_id'] == user_id
        assert updated_review['place_id'] == place_id
        print("   ✅ Partial update successful!")
        
        # Step 3: Test full update
        print("\n3. Testing full update...")
        
        # Create another user to test user_id update
        user2_data = {
            "first_name": "Bob",
            "last_name": "Wilson", 
            "email": "bob.wilson@example.com"
        }
        user2_response = client.post('/api/v1/users/', 
                                   data=json.dumps(user2_data),
                                   content_type='application/json')
        user2_id = user2_response.get_json()['id']
        print(f"   Created second user: {user2_id}")
        
        # Create another place
        place2_data = {
            "title": "Cozy Cottage",
            "description": "A cozy cottage in the countryside",
            "price": 200.0,
            "latitude": 41.8781,
            "longitude": -87.6298,
            "owner_id": user2_id,
            "amenities": [amenity_id]
        }
        place2_response = client.post('/api/v1/places/',
                                    data=json.dumps(place2_data),
                                    content_type='application/json')
        place2_id = place2_response.get_json()['id']
        print(f"   Created second place: {place2_id}")
        
        full_update_data = {
            "text": "This cottage is absolutely perfect!",
            "rating": 5,
            "user_id": user2_id,
            "place_id": place2_id
        }
        
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(full_update_data),
                            content_type='application/json')
        print(f"   Status Code: {response.status_code}")
        fully_updated_review = response.get_json()
        print(f"   Fully updated review: "
              f"{json.dumps(fully_updated_review, indent=4)}")
        
        # Verify all changes
        assert response.status_code == 200
        assert fully_updated_review['text'] == full_update_data['text']
        assert fully_updated_review['rating'] == full_update_data['rating']
        assert fully_updated_review['user_id'] == user2_id
        assert fully_updated_review['place_id'] == place2_id
        print("   ✅ Full update successful!")
        
        # Step 4: Test error cases
        print("\n4. Testing error cases...")
        
        # Test non-existent review
        response = client.put('/api/v1/reviews/non-existent-id',
                            data=json.dumps({"text": "Test"}),
                            content_type='application/json')
        print(f"   Non-existent review - Status: {response.status_code}, "
              f"Response: {response.get_json()}")
        assert response.status_code == 404
        
        # Test invalid rating
        invalid_rating_data = {"rating": 6}
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(invalid_rating_data),
                            content_type='application/json')
        print(f"   Invalid rating - Status: {response.status_code}, "
              f"Response: {response.get_json()}")
        assert response.status_code == 400
        
        # Test non-existent user
        invalid_user_data = {"user_id": "non-existent-user"}
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(invalid_user_data),
                            content_type='application/json')
        print(f"   Non-existent user - Status: {response.status_code}, "
              f"Response: {response.get_json()}")
        assert response.status_code == 400
        
        # Test non-existent place
        invalid_place_data = {"place_id": "non-existent-place"}
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(invalid_place_data),
                            content_type='application/json')
        print(f"   Non-existent place - Status: {response.status_code}, "
              f"Response: {response.get_json()}")
        assert response.status_code == 400
        
        print("   ✅ All error cases handled correctly!")
        
        # Step 5: Verify updated_at timestamp changed
        print("\n5. Testing updated_at timestamp...")
        original_updated_at = updated_review['updated_at']
        
        # Small update
        timestamp_test_data = {"text": "Final review text"}
        response = client.put(f'/api/v1/reviews/{review_id}',
                            data=json.dumps(timestamp_test_data),
                            content_type='application/json')
        final_review = response.get_json()
        new_updated_at = final_review['updated_at']
        
        print(f"   Original updated_at: {original_updated_at}")
        print(f"   New updated_at: {new_updated_at}")
        assert new_updated_at != original_updated_at
        print("   ✅ Timestamp updated correctly!")
        
        print("\n🎉 All PUT /api/v1/reviews/<review_id> tests passed!")

if __name__ == "__main__":
    test_update_review()
