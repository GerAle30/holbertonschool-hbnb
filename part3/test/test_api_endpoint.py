#!/usr/bin/env python3
"""
Comprehensive unit tests for HBnB API endpoints
Tests all CRUD operations for Users, Amenities, Places, and Reviews
"""

import unittest
import json
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User endpoints"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Test data
        self.valid_user = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }

        self.invalid_user = {
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        }

    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users/',
                                    json=self.valid_user,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], self.valid_user['first_name'])
        self.assertEqual(data['email'], self.valid_user['email'])
        self.assertIn('created_at', data)

    def test_create_user_invalid_data(self):
        """Test user creation with invalid data"""
        response = self.client.post('/api/v1/users/',
                                    json=self.invalid_user,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_user_missing_fields(self):
        """Test user creation with missing required fields"""
        incomplete_user = {"first_name": "John"}

        response = self.client.post('/api/v1/users/',
                                    json=incomplete_user,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test retrieving all users"""
        # Create a user first
        self.client.post('/api/v1/users/', json=self.valid_user)

        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_user_by_id(self):
        """Test retrieving a specific user by ID"""
        # Create a user first
        create_response = self.client.post(
            '/api/v1/users/', json=self.valid_user)
        created_user = json.loads(create_response.data)
        user_id = created_user['id']

        # Get the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['email'], self.valid_user['email'])

    def test_get_nonexistent_user(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/fake-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test updating a user"""
        # Create a user first
        create_response = self.client.post(
            '/api/v1/users/', json=self.valid_user)
        created_user = json.loads(create_response.data)
        user_id = created_user['id']

        # Update the user
        update_data = {"first_name": "Updated", "last_name": "Name"}
        response = self.client.put(f'/api/v1/users/{user_id}',
                                   json=update_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity endpoints"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        self.valid_amenity = {"name": "WiFi"}

    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities/',
                                    json=self.valid_amenity,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], self.valid_amenity['name'])

    def test_create_amenity_invalid_data(self):
        """Test amenity creation with invalid data"""
        invalid_amenity = {"name": ""}

        response = self.client.post('/api/v1/amenities/',
                                    json=invalid_amenity,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        # Create an amenity first
        self.client.post('/api/v1/amenities/', json=self.valid_amenity)

        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_amenity_by_id(self):
        """Test retrieving a specific amenity by ID"""
        # Create an amenity first
        create_response = self.client.post(
            '/api/v1/amenities/', json=self.valid_amenity)
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']

        # Get the amenity by ID
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['id'], amenity_id)

    def test_update_amenity(self):
        """Test updating an amenity"""
        # Create an amenity first
        create_response = self.client.post(
            '/api/v1/amenities/', json=self.valid_amenity)
        created_amenity = json.loads(create_response.data)
        amenity_id = created_amenity['id']

        # Update the amenity
        update_data = {"name": "Swimming Pool"}
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
                                   json=update_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Swimming Pool')


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place endpoints"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Create a user and amenity for place testing
        user_data = {
            "first_name": "John",
            "last_name": "Owner",
            "email": "owner@example.com"
        }
        user_response = self.client.post('/api/v1/users/', json=user_data)
        self.user = json.loads(user_response.data)

        amenity_data = {"name": "WiFi"}
        amenity_response = self.client.post(
            '/api/v1/amenities/', json=amenity_data)
        self.amenity = json.loads(amenity_response.data)

        self.valid_place = {
            "title": "Beautiful Apartment",
            "description": "A lovely place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user['id'],
            "amenities": [self.amenity['id']]
        }

    def test_create_place_success(self):
        """Test successful place creation"""
        response = self.client.post('/api/v1/places/',
                                    json=self.valid_place,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], self.valid_place['title'])
        self.assertEqual(data['price'], self.valid_place['price'])

    def test_create_place_invalid_owner(self):
        """Test place creation with invalid owner"""
        invalid_place = self.valid_place.copy()
        invalid_place['owner_id'] = 'fake-owner-id'

        response = self.client.post('/api/v1/places/',
                                    json=invalid_place,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_price(self):
        """Test place creation with invalid price"""
        invalid_place = self.valid_place.copy()
        invalid_place['price'] = -10.0

        response = self.client.post('/api/v1/places/',
                                    json=invalid_place,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieving all places"""
        # Create a place first
        self.client.post('/api/v1/places/', json=self.valid_place)

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        """Test retrieving a specific place by ID"""
        # Create a place first
        create_response = self.client.post(
            '/api/v1/places/', json=self.valid_place)
        created_place = json.loads(create_response.data)
        place_id = created_place['id']

        # Get the place by ID
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['id'], place_id)
        self.assertIn('owner', data)
        self.assertIn('amenities', data)

    def test_update_place(self):
        """Test updating a place"""
        # Create a place first
        create_response = self.client.post(
            '/api/v1/places/', json=self.valid_place)
        created_place = json.loads(create_response.data)
        place_id = created_place['id']

        # Update the place
        update_data = {"title": "Updated Title", "price": 150.0}
        response = self.client.put(f'/api/v1/places/{place_id}',
                                   json=update_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['price'], 150.0)


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review endpoints"""

    def setUp(self):
        """Set up test client and test data"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Create user, amenity, and place for review testing
        user_data = {
            "first_name": "John",
            "last_name": "Owner",
            "email": "owner@example.com"
        }
        user_response = self.client.post('/api/v1/users/', json=user_data)
        self.user = json.loads(user_response.data)

        reviewer_data = {
            "first_name": "Jane",
            "last_name": "Reviewer",
            "email": "reviewer@example.com"
        }
        reviewer_response = self.client.post(
            '/api/v1/users/', json=reviewer_data)
        self.reviewer = json.loads(reviewer_response.data)

        amenity_data = {"name": "WiFi"}
        amenity_response = self.client.post(
            '/api/v1/amenities/', json=amenity_data)
        self.amenity = json.loads(amenity_response.data)

        place_data = {
            "title": "Test Place",
            "description": "A place for testing",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user['id'],
            "amenities": [self.amenity['id']]
        }
        place_response = self.client.post('/api/v1/places/', json=place_data)
        self.place = json.loads(place_response.data)

        self.valid_review = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.reviewer['id'],
            "place_id": self.place['id']
        }

    def test_create_review_success(self):
        """Test successful review creation"""
        response = self.client.post('/api/v1/reviews/',
                                    json=self.valid_review,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], self.valid_review['text'])
        self.assertEqual(data['rating'], self.valid_review['rating'])

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating"""
        invalid_review = self.valid_review.copy()
        invalid_review['rating'] = 6  # Invalid rating

        response = self.client.post('/api/v1/reviews/',
                                    json=invalid_review,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_create_review_nonexistent_user(self):
        """Test review creation with non-existent user"""
        invalid_review = self.valid_review.copy()
        invalid_review['user_id'] = 'fake-user-id'

        response = self.client.post('/api/v1/reviews/',
                                    json=invalid_review,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        # Create a review first
        self.client.post('/api/v1/reviews/', json=self.valid_review)

        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_review_by_id(self):
        """Test retrieving a specific review by ID"""
        # Create a review first
        create_response = self.client.post(
            '/api/v1/reviews/', json=self.valid_review)
        created_review = json.loads(create_response.data)
        review_id = created_review['id']

        # Get the review by ID
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['id'], review_id)

    def test_get_reviews_by_place(self):
        """Test retrieving reviews for a specific place"""
        # Create a review first
        self.client.post('/api/v1/reviews/', json=self.valid_review)

        # Get reviews for the place
        response = self.client.get(
            f'/api/v1/places/{self.place["id"]}/reviews')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:  # If reviews exist
            self.assertEqual(data[0]['place_id'], self.place['id'])

    def test_update_review(self):
        """Test updating a review"""
        # Create a review first
        create_response = self.client.post(
            '/api/v1/reviews/', json=self.valid_review)
        created_review = json.loads(create_response.data)
        review_id = created_review['id']

        # Update the review
        update_data = {"text": "Updated review text", "rating": 4}
        response = self.client.put(f'/api/v1/reviews/{review_id}',
                                   json=update_data,
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Updated review text')
        self.assertEqual(data['rating'], 4)

    def test_delete_review(self):
        """Test deleting a review"""
        # Create a review first
        create_response = self.client.post(
            '/api/v1/reviews/', json=self.valid_review)
        created_review = json.loads(create_response.data)
        review_id = created_review['id']

        # Delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)


class TestEndpointIntegration(unittest.TestCase):
    """Integration tests for endpoint interactions"""

    def setUp(self):
        """Set up test client"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_place_with_reviews_integration(self):
        """Test that place details include reviews"""
        # Create user
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"}
        user_response = self.client.post('/api/v1/users/', json=user_data)
        user = json.loads(user_response.data)

        # Create amenity
        amenity_data = {"name": "WiFi"}
        amenity_response = self.client.post(
            '/api/v1/amenities/', json=amenity_data)
        amenity = json.loads(amenity_response.data)

        # Create place
        place_data = {
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user['id'],
            "amenities": [amenity['id']]
        }
        place_response = self.client.post('/api/v1/places/', json=place_data)
        place = json.loads(place_response.data)

        # Create review
        review_data = {
            "text": "Great place!",
            "rating": 5,
            "user_id": user['id'],
            "place_id": place['id']
        }
        self.client.post('/api/v1/reviews/', json=review_data)

        # Get place details and verify reviews are included
        response = self.client.get(f'/api/v1/places/{place["id"]}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('reviews', data)
        self.assertGreater(len(data['reviews']), 0)


if __name__ == '__main__':
    # Create test directory if it doesn't exist
    import os
    os.makedirs('tests', exist_ok=True)

    # Run tests
    unittest.main(verbosity=2)
