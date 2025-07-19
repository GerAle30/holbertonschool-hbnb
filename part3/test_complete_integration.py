#!/usr/bin/env python3
"""
Comprehensive test script to verify the complete integration of all specialized repositories
(User, Place, Review, Amenity) and their corresponding facade methods.
"""

from app import create_app, db
from app.services.facade import HBnBFacade

def test_complete_integration():
    """Test the complete integration of all repositories and facade methods."""
    
    app = create_app()
    
    with app.app_context():
        print("Testing Complete Repository and Facade Integration")
        print("=" * 60)
        
        # Initialize the facade
        facade = HBnBFacade()
        
        # Recreate database for clean state
        print("\n1. Setting up database...")
        try:
            db.drop_all()
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Database setup failed: {e}")
            return
        
        # Test User operations
        print("\n2. Testing User operations...")
        try:
            # Create users
            admin_user = facade.create_user({
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@test.com',
                'password': 'admin123',
                'is_admin': True
            })
            
            regular_user = facade.create_user({
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@test.com',
                'password': 'user123',
                'is_admin': False
            })
            
            print(f"Created users: {admin_user.email}, {regular_user.email}")
            
            # Test user repository methods
            user_stats = facade.get_user_statistics()
            print(f"User statistics: {user_stats}")
            
        except Exception as e:
            print(f"User operations failed: {e}")
            return
        
        # Test Amenity operations
        print("\n3. Testing Amenity operations...")
        try:
            # Create amenities
            wifi = facade.create_amenity({'name': 'WiFi'})
            pool = facade.create_amenity({'name': 'Swimming Pool'})
            parking = facade.create_amenity({'name': 'Parking'})
            gym = facade.create_amenity({'name': 'Gym'})
            
            print(f"Created amenities: {[a.name for a in [wifi, pool, parking, gym]]}")
            
            # Test amenity repository methods
            amenity_stats = facade.get_amenity_statistics()
            print(f"Amenity statistics: {amenity_stats}")
            
            recent_amenities = facade.get_recent_amenities(2)
            print(f"Recent amenities: {[a.name for a in recent_amenities]}")
            
        except Exception as e:
            print(f"Amenity operations failed: {e}")
            return
        
        # Test Place operations
        print("\n4. Testing Place operations...")
        try:
            # Create places
            place1 = facade.create_place({
                'title': 'Modern Apartment',
                'description': 'A beautiful modern apartment in downtown',
                'price': 150.0,
                'latitude': 40.7128,
                'longitude': -74.0060,
                'owner_id': regular_user.id,
                'amenities': [wifi.id, parking.id]
            })
            
            place2 = facade.create_place({
                'title': 'Beach House',
                'description': 'Relaxing beach house with ocean view',
                'price': 300.0,
                'latitude': 25.7617,
                'longitude': -80.1918,
                'owner_id': admin_user.id,
                'amenities': [wifi.id, pool.id, gym.id]
            })
            
            place3 = facade.create_place({
                'title': 'Budget Room',
                'description': 'Simple and clean budget accommodation',
                'price': 75.0,
                'latitude': 34.0522,
                'longitude': -118.2437,
                'owner_id': regular_user.id,
                'amenities': [wifi.id]
            })
            
            print(f"Created places: {[p.title for p in [place1, place2, place3]]}")
            
            # Test place repository methods
            place_stats = facade.get_place_statistics()
            print(f"Place statistics: {place_stats}")
            
            # Test price range queries
            expensive_places = facade.get_places_by_price_range(200, 400)
            print(f"Expensive places (200-400): {[p.title for p in expensive_places]}")
            
            budget_places = facade.get_places_by_price_range(50, 100)
            print(f"Budget places (50-100): {[p.title for p in budget_places]}")
            
            # Test location-based queries
            nearby_places = facade.get_places_by_location(40.7128, -74.0060, 50)
            print(f"Places near NYC: {[p.title for p in nearby_places]}")
            
            # Test title search
            modern_places = facade.search_places_by_title('Modern')
            print(f"Places with 'Modern' in title: {[p.title for p in modern_places]}")
            
        except Exception as e:
            print(f"Place operations failed: {e}")
            return
        
        # Test Review operations
        print("\n5. Testing Review operations...")
        try:
            # Create reviews
            review1 = facade.create_review({
                'text': 'Excellent place! Very clean and comfortable.',
                'rating': 5,
                'user_id': regular_user.id,
                'place_id': place2.id
            })
            
            review2 = facade.create_review({
                'text': 'Good location but a bit noisy at night.',
                'rating': 3,
                'user_id': admin_user.id,
                'place_id': place1.id
            })
            
            review3 = facade.create_review({
                'text': 'Great value for money. Basic but clean.',
                'rating': 4,
                'user_id': admin_user.id,
                'place_id': place3.id
            })
            
            review4 = facade.create_review({
                'text': 'Amazing beach house with perfect view!',
                'rating': 5,
                'user_id': regular_user.id,
                'place_id': place2.id
            })
            
            print(f"Created {len([review1, review2, review3, review4])} reviews")
            
            # Test review repository methods
            review_stats = facade.get_review_statistics()
            print(f"Review statistics: {review_stats}")
            
            # Test rating queries
            high_rated = facade.get_high_rated_reviews(4)
            print(f"High-rated reviews (4+): {len(high_rated)}")
            
            five_star = facade.get_reviews_by_rating(5)
            print(f"Five-star reviews: {len(five_star)}")
            
            # Test text search
            clean_reviews = facade.search_reviews_by_text('clean')
            print(f"Reviews mentioning 'clean': {len(clean_reviews)}")
            
        except Exception as e:
            print(f"Review operations failed: {e}")
            return
        
        # Test cross-entity operations
        print("\n6. Testing cross-entity operations...")
        try:
            # Get reviews for a specific place
            place2_reviews = facade.get_reviews_by_place(place2.id)
            print(f"Reviews for {place2.title}: {len(place2_reviews)}")
            
            # Test comprehensive statistics
            print("\n7. System-wide statistics:")
            print(f"Users: {facade.get_user_statistics()}")
            print(f"Places: {facade.get_place_statistics()}")
            print(f"Reviews: {facade.get_review_statistics()}")
            print(f"Amenities: {facade.get_amenity_statistics()}")
            
        except Exception as e:
            print(f"Cross-entity operations failed: {e}")
            return
        
        # Test repository-specific advanced queries
        print("\n8. Testing advanced repository queries...")
        try:
            # Place repository advanced queries
            ordered_by_price = facade.get_places_ordered_by_price(ascending=True)
            print(f"Places by price (asc): {[(p.title, p.price) for p in ordered_by_price]}")
            
            recent_places = facade.get_recent_places(2)
            print(f"Recent places: {[p.title for p in recent_places]}")
            
            # Review repository advanced queries
            rating_range = facade.get_reviews_by_rating_range(3, 4)
            print(f"Reviews with rating 3-4: {len(rating_range)}")
            
            recent_reviews = facade.get_recent_reviews(3)
            print(f"Recent reviews: {len(recent_reviews)}")
            
            # User repository advanced queries
            recent_users = facade.get_recent_users(2)
            print(f"Recent users: {[u.email for u in recent_users]}")
            
            admin_users = facade.get_all_admin_users()
            print(f"Admin users: {[u.email for u in admin_users]}")
            
        except Exception as e:
            print(f"Advanced queries failed: {e}")
        
        print("\n" + "=" * 60)
        print("Complete integration test finished!")
        print("\nSummary of implemented features:")
        print("- User management with specialized UserRepository")
        print("- Place management with location and price queries")
        print("- Review management with rating analytics")
        print("- Amenity management with uniqueness validation")
        print("- Cross-entity operations and comprehensive statistics")
        print("- All repositories follow the same pattern as UserRepository")

if __name__ == '__main__':
    test_complete_integration()
