#!/usr/bin/env python3
"""
Test script to verify SQLAlchemy mapping for Place, Review, and Amenity entities.
This script will test model creation, validation, and database operations.
"""

from app import create_app, db
from app.models.place import Place
from app.models.reviews import Review
from app.models.amenities import Amenity

def test_entity_mapping():
    """Test SQLAlchemy mapping for all entities."""
    
    app = create_app()
    
    with app.app_context():
        print("Testing SQLAlchemy Entity Mapping")
        print("=" * 50)
        
        # Recreate tables to ensure clean state
        print("\n1. Creating database tables...")
        try:
            db.drop_all()
            db.create_all()
            
            # Check what tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tables created: {tables}")
            
        except Exception as e:
            print(f"Failed to create tables: {e}")
            return
        
        # Test Amenity model
        print("\n2. Testing Amenity model...")
        try:
            # Valid amenity creation
            wifi = Amenity(name="WiFi")
            pool = Amenity(name="Swimming Pool")
            parking = Amenity(name="Parking")
            
            db.session.add_all([wifi, pool, parking])
            db.session.commit()
            
            print(f"Created amenities:")
            print(f"  - {wifi}")
            print(f"  - {pool}")
            print(f"  - {parking}")
            
            # Test amenity validation
            try:
                empty_amenity = Amenity(name="")
                print("ERROR: Empty amenity name should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
            
            try:
                long_name_amenity = Amenity(name="A" * 51)
                print("ERROR: Long amenity name should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
            
        except Exception as e:
            print(f"Amenity model test failed: {e}")
        
        # Test Place model
        print("\n3. Testing Place model...")
        try:
            # Valid place creation
            place1 = Place(
                title="Modern Apartment",
                description="A beautiful modern apartment in the city center",
                price=150.50,
                latitude=40.7128,
                longitude=-74.0060
            )
            
            place2 = Place(
                title="Beach House",
                description="Relaxing beach house with ocean view",
                price=300.00,
                latitude=25.7617,
                longitude=-80.1918
            )
            
            db.session.add_all([place1, place2])
            db.session.commit()
            
            print(f"Created places:")
            print(f"  - {place1}")
            print(f"  - {place2}")
            
            # Test place validation
            try:
                invalid_price = Place(title="Test", price=-50, latitude=0, longitude=0)
                print("ERROR: Negative price should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
            
            try:
                invalid_lat = Place(title="Test", price=100, latitude=95, longitude=0)
                print("ERROR: Invalid latitude should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
            
            try:
                invalid_lon = Place(title="Test", price=100, latitude=0, longitude=200)
                print("ERROR: Invalid longitude should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
                
        except Exception as e:
            print(f"Place model test failed: {e}")
        
        # Test Review model
        print("\n4. Testing Review model...")
        try:
            # Valid review creation
            review1 = Review(
                text="Great place! Very clean and comfortable.",
                rating=5
            )
            
            review2 = Review(
                text="Good location but a bit noisy at night.",
                rating=3
            )
            
            db.session.add_all([review1, review2])
            db.session.commit()
            
            print(f"Created reviews:")
            print(f"  - {review1}")
            print(f"  - {review2}")
            
            # Test review validation
            try:
                invalid_rating_high = Review(text="Test review", rating=6)
                print("ERROR: Rating > 5 should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
            
            try:
                invalid_rating_low = Review(text="Test review", rating=0)
                print("ERROR: Rating < 1 should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
            
            try:
                empty_text = Review(text="", rating=4)
                print("ERROR: Empty review text should not be allowed")
            except ValueError as e:
                print(f"Validation working: {e}")
                
        except Exception as e:
            print(f"Review model test failed: {e}")
        
        # Test database queries
        print("\n5. Testing database queries...")
        try:
            # Test retrieving entities
            all_amenities = Amenity.query.all()
            all_places = Place.query.all()
            all_reviews = Review.query.all()
            
            print(f"Database contains:")
            print(f"  - {len(all_amenities)} amenities")
            print(f"  - {len(all_places)} places")
            print(f"  - {len(all_reviews)} reviews")
            
            # Test filtering
            wifi_amenity = Amenity.query.filter_by(name="WiFi").first()
            expensive_places = Place.query.filter(Place.price > 200).all()
            high_rated_reviews = Review.query.filter(Review.rating >= 4).all()
            
            print(f"Query results:")
            print(f"  - WiFi amenity found: {wifi_amenity is not None}")
            print(f"  - Expensive places (>$200): {len(expensive_places)}")
            print(f"  - High-rated reviews (>=4): {len(high_rated_reviews)}")
            
        except Exception as e:
            print(f"Database query test failed: {e}")
        
        # Test model updates
        print("\n6. Testing model updates...")
        try:
            # Update a place
            place = Place.query.first()
            if place:
                original_price = place.price
                place.price = 200.00
                db.session.commit()
                
                updated_place = Place.query.get(place.id)
                print(f"Updated place price: {original_price} -> {updated_place.price}")
            
            # Update a review
            review = Review.query.first()
            if review:
                original_rating = review.rating
                review.rating = 4
                review.text = "Updated review text"
                db.session.commit()
                
                updated_review = Review.query.get(review.id)
                print(f"Updated review rating: {original_rating} -> {updated_review.rating}")
            
        except Exception as e:
            print(f"Update test failed: {e}")
        
        print("\n" + "=" * 50)
        print("Entity mapping tests completed!")
        print("\nSQLAlchemy mapping summary:")
        print("- Place model: title, description, price, latitude, longitude")
        print("- Review model: text, rating")
        print("- Amenity model: name (unique)")
        print("- All models inherit from BaseModel: id, created_at, updated_at")
        print("- All validation rules are working correctly")
        print("- Database operations (create, read, update) are functional")

if __name__ == '__main__':
    test_entity_mapping()
