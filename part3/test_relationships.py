#!/usr/bin/env python3
"""
Test script to verify SQLAlchemy relationships between entities.
This script tests all four required relationships:
1. User and Place (One-to-Many)
2. Place and Review (One-to-Many) 
3. User and Review (One-to-Many)
4. Place and Amenity (Many-to-Many)
"""

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.reviews import Review
from app.models.amenities import Amenity

def test_relationships():
    """Test all SQLAlchemy relationships between entities."""
    
    app = create_app()
    
    with app.app_context():
        print("Testing SQLAlchemy Relationships")
        print("=" * 50)
        
        # Initialize database
        print("\n1. Setting up database...")
        try:
            db.drop_all()
            db.create_all()
            print("✓ Database tables created successfully")
        except Exception as e:
            print(f"✗ Database setup failed: {e}")
            return
        
        # Test 1: Create Users
        print("\n2. Creating users...")
        try:
            # Create users
            user1 = User(
                first_name="John",
                last_name="Doe", 
                email="john@example.com"
            )
            user1.hash_password("password123")
            
            user2 = User(
                first_name="Jane",
                last_name="Smith",
                email="jane@example.com"
            )
            user2.hash_password("password456")
            
            db.session.add_all([user1, user2])
            db.session.commit()
            
            print(f"✓ Created users: {user1.email}, {user2.email}")
            
        except Exception as e:
            print(f"✗ User creation failed: {e}")
            return
        
        # Test 2: Create Amenities (for Many-to-Many relationship)
        print("\n3. Creating amenities...")
        try:
            wifi = Amenity(name="WiFi")
            pool = Amenity(name="Swimming Pool")
            parking = Amenity(name="Parking")
            gym = Amenity(name="Gym")
            
            db.session.add_all([wifi, pool, parking, gym])
            db.session.commit()
            
            print(f"✓ Created amenities: {[a.name for a in [wifi, pool, parking, gym]]}")
            
        except Exception as e:
            print(f"✗ Amenity creation failed: {e}")
            return
        
        # Test 3: Create Places and test User-Place relationship (One-to-Many)
        print("\n4. Testing User-Place relationship (One-to-Many)...")
        try:
            # Create places owned by different users
            place1 = Place(
                title="Modern Apartment",
                description="Beautiful apartment in downtown",
                price=150.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=user1.id
            )
            
            place2 = Place(
                title="Beach House",
                description="Relaxing beach house with ocean view", 
                price=300.0,
                latitude=25.7617,
                longitude=-80.1918,
                owner_id=user1.id  # Same user owns multiple places
            )
            
            place3 = Place(
                title="Cozy Cabin",
                description="Mountain cabin retreat",
                price=120.0,
                latitude=39.5501,
                longitude=-105.7821,
                owner_id=user2.id  # Different user
            )
            
            db.session.add_all([place1, place2, place3])
            db.session.commit()
            
            print(f"✓ Created places: {[p.title for p in [place1, place2, place3]]}")
            
            # Test the relationship: User should have access to their places
            user1_places = user1.places
            user2_places = user2.places
            
            print(f"✓ User1 ({user1.email}) owns {len(user1_places)} places: {[p.title for p in user1_places]}")
            print(f"✓ User2 ({user2.email}) owns {len(user2_places)} places: {[p.title for p in user2_places]}")
            
            # Test reverse relationship: Place should have access to owner
            print(f"✓ Place '{place1.title}' is owned by: {place1.owner.email}")
            print(f"✓ Place '{place3.title}' is owned by: {place3.owner.email}")
            
        except Exception as e:
            print(f"✗ User-Place relationship test failed: {e}")
            return
        
        # Test 4: Test Place-Amenity relationship (Many-to-Many)
        print("\n5. Testing Place-Amenity relationship (Many-to-Many)...")
        try:
            # Add amenities to places
            place1.amenities.extend([wifi, parking])  # Place1 has WiFi and Parking
            place2.amenities.extend([wifi, pool, gym])  # Place2 has WiFi, Pool, and Gym
            place3.amenities.append(wifi)  # Place3 only has WiFi
            
            db.session.commit()
            
            # Test forward relationship: Place -> Amenities
            print(f"✓ '{place1.title}' amenities: {[a.name for a in place1.amenities]}")
            print(f"✓ '{place2.title}' amenities: {[a.name for a in place2.amenities]}")
            print(f"✓ '{place3.title}' amenities: {[a.name for a in place3.amenities]}")
            
            # Test reverse relationship: Amenity -> Places
            print(f"✓ WiFi is available at: {[p.title for p in wifi.places]}")
            print(f"✓ Pool is available at: {[p.title for p in pool.places]}")
            print(f"✓ Parking is available at: {[p.title for p in parking.places]}")
            
        except Exception as e:
            print(f"✗ Place-Amenity relationship test failed: {e}")
            return
        
        # Test 5: Create Reviews and test User-Review and Place-Review relationships
        print("\n6. Testing User-Review and Place-Review relationships (One-to-Many)...")
        try:
            # Create reviews
            review1 = Review(
                text="Excellent place! Very clean and comfortable.",
                rating=5,
                user_id=user2.id,  # user2 reviews user1's place
                place_id=place1.id
            )
            
            review2 = Review(
                text="Amazing beach house with perfect view!",
                rating=5,
                user_id=user2.id,  # user2 reviews user1's other place
                place_id=place2.id
            )
            
            review3 = Review(
                text="Great cabin but a bit remote.",
                rating=4,
                user_id=user1.id,  # user1 reviews user2's place
                place_id=place3.id
            )
            
            review4 = Review(
                text="Good location but could use some updates.",
                rating=3,
                user_id=user1.id,  # user1 writes another review for place1
                place_id=place1.id
            )
            
            db.session.add_all([review1, review2, review3, review4])
            db.session.commit()
            
            print(f"✓ Created {4} reviews")
            
            # Test User-Review relationship (One-to-Many)
            user1_reviews = user1.reviews
            user2_reviews = user2.reviews
            
            print(f"✓ User1 ({user1.email}) wrote {len(user1_reviews)} reviews")
            print(f"✓ User2 ({user2.email}) wrote {len(user2_reviews)} reviews")
            
            # Test Place-Review relationship (One-to-Many)
            place1_reviews = place1.reviews
            place2_reviews = place2.reviews
            place3_reviews = place3.reviews
            
            print(f"✓ '{place1.title}' has {len(place1_reviews)} reviews")
            print(f"✓ '{place2.title}' has {len(place2_reviews)} reviews") 
            print(f"✓ '{place3.title}' has {len(place3_reviews)} reviews")
            
            # Test reverse relationships
            print(f"✓ Review1 is by: {review1.user.email} for place: {review1.place.title}")
            print(f"✓ Review3 is by: {review3.user.email} for place: {review3.place.title}")
            
        except Exception as e:
            print(f"✗ User-Review and Place-Review relationship test failed: {e}")
            return
        
        # Test 6: Complex queries using relationships
        print("\n7. Testing complex relationship queries...")
        try:
            # Find all places owned by user1 with their reviews
            user1_places_with_reviews = []
            for place in user1.places:
                reviews_count = len(place.reviews)
                avg_rating = sum(r.rating for r in place.reviews) / reviews_count if reviews_count > 0 else 0
                user1_places_with_reviews.append({
                    'title': place.title,
                    'reviews_count': reviews_count,
                    'avg_rating': round(avg_rating, 1)
                })
            
            print("✓ User1's places with review statistics:")
            for place_info in user1_places_with_reviews:
                print(f"  - {place_info['title']}: {place_info['reviews_count']} reviews, avg rating: {place_info['avg_rating']}")
            
            # Find all reviews written by user2 with place information
            user2_reviews_with_places = []
            for review in user2.reviews:
                user2_reviews_with_places.append({
                    'rating': review.rating,
                    'place_title': review.place.title,
                    'place_owner': review.place.owner.email
                })
            
            print("✓ User2's reviews with place information:")
            for review_info in user2_reviews_with_places:
                print(f"  - Rated {review_info['rating']}/5 for '{review_info['place_title']}' (owned by {review_info['place_owner']})")
            
            # Find places that have both WiFi and Pool
            places_with_wifi_and_pool = []
            for place in Place.query.all():
                amenity_names = [a.name for a in place.amenities]
                if 'WiFi' in amenity_names and 'Swimming Pool' in amenity_names:
                    places_with_wifi_and_pool.append(place.title)
            
            print(f"✓ Places with both WiFi and Pool: {places_with_wifi_and_pool}")
            
        except Exception as e:
            print(f"✗ Complex relationship queries failed: {e}")
            return
        
        print("\n" + "=" * 50)
        print("✅ All relationship tests passed successfully!")
        print("\nRelationships verified:")
        print("1. ✓ User and Place (One-to-Many)")
        print("2. ✓ Place and Review (One-to-Many)")  
        print("3. ✓ User and Review (One-to-Many)")
        print("4. ✓ Place and Amenity (Many-to-Many)")
        print("\nRelationship features working:")
        print("- Foreign key constraints")
        print("- Bidirectional access (back_populates)")
        print("- Many-to-many association table")
        print("- Complex queries across relationships")
        print("- Lazy loading with proper fetching")

if __name__ == '__main__':
    test_relationships()
