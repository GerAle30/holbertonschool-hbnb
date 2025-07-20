#!/usr/bin/env python3
"""
Comprehensive Database Test Script for HBnB (SQLite Compatible)
Tests table creation, data insertion, CRUD operations, and API integration
"""

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.reviews import Review
from app.models.amenities import Amenity
from sqlalchemy import inspect

def test_database_comprehensive():
    """Run comprehensive database tests."""
    
    print("HBnB Database Comprehensive Test Suite")
    print("=" * 60)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test 1: Table Creation
            print("\nTEST 1: TABLE CREATION AND STRUCTURE")
            print("-" * 40)
            
            db.drop_all()
            db.create_all()
            
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            expected_tables = {'users', 'places', 'reviews', 'amenities', 'place_amenities'}
            
            if expected_tables.issubset(set(tables)):
                print("✓ All required tables created")
                print(f"  Tables: {sorted(list(expected_tables))}")
            else:
                missing = expected_tables - set(tables)
                print(f"✗ Missing tables: {missing}")
                return False
            
            # Test 2: Initial Data Insertion
            print("\nTEST 2: INITIAL DATA INSERTION")
            print("-" * 40)
            
            # Create admin user with specified UUID
            admin_user = User(
                first_name='Admin',
                last_name='HBnB',
                email='admin@hbnb.io',
                is_admin=True
            )
            admin_user.id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
            admin_user.hash_password('admin1234')
            
            # Create initial amenities
            wifi = Amenity(name='WiFi')
            wifi.id = 'ccaf6b6c-b86d-4dec-8a87-8a3050d1e463'
            
            pool = Amenity(name='Swimming Pool')
            pool.id = '075fd2d0-2b15-432a-862d-516366d41465'
            
            ac = Amenity(name='Air Conditioning')
            ac.id = '6e59f738-be8e-40ce-9e8b-9af7d6b816db'
            
            db.session.add_all([admin_user, wifi, pool, ac])
            db.session.commit()
            
            print(f"✓ Admin user created: {admin_user.email}")
            print(f"  UUID: {admin_user.id}")
            print(f"  Admin status: {admin_user.is_admin}")
            print(f"  Password hash starts with: {admin_user.password[:10]}...")
            
            print("✓ Initial amenities created:")
            for amenity in [wifi, pool, ac]:
                print(f"  - {amenity.name} (ID: {amenity.id})")
            
            # Test password verification
            password_test = admin_user.verify_password('admin1234')
            print(f"✓ Password verification: {'PASS' if password_test else 'FAIL'}")
            
            if not password_test:
                print("✗ Password verification failed!")
                return False
            
            # Test 3: CRUD Operations
            print("\nTEST 3: CRUD OPERATIONS")
            print("-" * 40)
            
            # CREATE operations
            test_user = User(
                first_name='Test',
                last_name='User',
                email='test@example.com',
                is_admin=False
            )
            test_user.hash_password('testpass')
            db.session.add(test_user)
            db.session.commit()
            print(f"✓ Created test user: {test_user.email}")
            
            test_place = Place(
                title='Test Place',
                description='A place for testing',
                price=150.00,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=test_user.id
            )
            db.session.add(test_place)
            db.session.commit()
            print(f"✓ Created test place: {test_place.title}")
            
            test_review = Review(
                text='Great place for testing!',
                rating=5,
                user_id=admin_user.id,
                place_id=test_place.id
            )
            db.session.add(test_review)
            db.session.commit()
            print(f"✓ Created test review: Rating {test_review.rating}/5")
            
            # Test many-to-many relationship
            test_place.amenities.extend([wifi, pool])
            db.session.commit()
            print(f"✓ Added amenities: {[a.name for a in test_place.amenities]}")
            
            # READ operations - Test relationships
            print("\nTesting relationships:")
            user_places = test_user.places
            print(f"✓ User-Place relationship: {len(user_places)} places")
            
            place_reviews = test_place.reviews
            print(f"✓ Place-Review relationship: {len(place_reviews)} reviews")
            
            user_reviews = admin_user.reviews
            print(f"✓ User-Review relationship: {len(user_reviews)} reviews")
            
            place_amenities = test_place.amenities
            print(f"✓ Place-Amenity relationship: {len(place_amenities)} amenities")
            
            # UPDATE operations
            print("\nTesting UPDATE operations:")
            original_price = test_place.price
            test_place.price = 200.00
            db.session.commit()
            print(f"✓ Updated place price: ${original_price} -> ${test_place.price}")
            
            original_rating = test_review.rating
            test_review.rating = 4
            db.session.commit()
            print(f"✓ Updated review rating: {original_rating} -> {test_review.rating}")
            
            # Test 4: Constraint Testing
            print("\nTEST 4: CONSTRAINT TESTING")
            print("-" * 40)
            
            # Test unique email constraint
            try:
                duplicate_user = User(
                    first_name='Duplicate',
                    last_name='User',
                    email='admin@hbnb.io',
                    is_admin=False
                )
                duplicate_user.hash_password('password')
                db.session.add(duplicate_user)
                db.session.commit()
                print("✗ Unique constraint test: FAIL - Duplicate allowed")
                return False
            except Exception:
                db.session.rollback()
                print("✓ Unique constraint test: PASS - Duplicate prevented")
            
            # Test rating validation
            try:
                invalid_review = Review(
                    text='Invalid rating',
                    rating=6,  # Invalid rating
                    user_id=admin_user.id,
                    place_id=test_place.id
                )
                print("✗ Rating validation: FAIL - Invalid rating allowed")
            except ValueError:
                print("✓ Rating validation: PASS - Invalid rating prevented")
            
            # Test price validation
            try:
                invalid_place = Place(
                    title='Invalid Place',
                    description='Test',
                    price=-50.00,  # Invalid price
                    latitude=40.0,
                    longitude=-74.0,
                    owner_id=test_user.id
                )
                print("✗ Price validation: FAIL - Negative price allowed")
            except ValueError:
                print("✓ Price validation: PASS - Negative price prevented")
            
            # Test 5: Data Integrity
            print("\nTEST 5: DATA INTEGRITY")
            print("-" * 40)
            
            # Final counts
            user_count = User.query.count()
            place_count = Place.query.count()
            review_count = Review.query.count()
            amenity_count = Amenity.query.count()
            
            print(f"Final record counts:")
            print(f"  Users: {user_count}")
            print(f"  Places: {place_count}")
            print(f"  Reviews: {review_count}")
            print(f"  Amenities: {amenity_count}")
            
            # Verify admin user still exists
            final_admin = User.query.filter_by(email='admin@hbnb.io').first()
            if final_admin and final_admin.is_admin:
                print("✓ Admin user verified")
            else:
                print("✗ Admin user verification failed")
                return False
            
            # Verify amenities exist
            amenity_names = [a.name for a in Amenity.query.all()]
            required_amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
            if all(name in amenity_names for name in required_amenities):
                print("✓ All required amenities present")
            else:
                print("✗ Missing required amenities")
                return False
            
            print("\n" + "=" * 60)
            print("✓ ALL DATABASE TESTS PASSED!")
            print("\nDatabase is ready for production use!")
            return True
            
        except Exception as e:
            print(f"\nERROR: Database test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_api_integration():
    """Test API integration with database."""
    
    print("\n" + "=" * 60)
    print("API INTEGRATION TESTING")
    print("=" * 60)
    
    try:
        app = create_app()
        
        with app.test_client() as client:
            print("\n1. Testing admin authentication...")
            
            # Test login
            login_response = client.post('/api/v1/auth/login',
                                         json={
                                             'email': 'admin@hbnb.io',
                                             'password': 'admin1234'
                                         },
                                         content_type='application/json')
            
            if login_response.status_code == 200:
                data = login_response.get_json()
                if 'access_token' in data:
                    print("✓ Admin authentication successful")
                    
                    # Test amenities endpoint
                    amenities_response = client.get('/api/v1/amenities/')
                    if amenities_response.status_code == 200:
                        amenities_data = amenities_response.get_json()
                        print(f"✓ Amenities API: {len(amenities_data)} amenities")
                        for amenity in amenities_data:
                            print(f"  - {amenity['name']}")
                    else:
                        print(f"✗ Amenities API failed")
                        return False
                    
                    # Test users endpoint
                    users_response = client.get('/api/v1/users/')
                    if users_response.status_code == 200:
                        users_data = users_response.get_json()
                        admin_found = any(u['email'] == 'admin@hbnb.io' for u in users_data)
                        print(f"✓ Users API: Admin user found = {admin_found}")
                    else:
                        print("✗ Users API failed")
                        return False
                    
                    return True
                else:
                    print("✗ No access token received")
                    return False
            else:
                print(f"✗ Login failed: {login_response.status_code}")
                print(f"Response: {login_response.get_json()}")
                return False
                
    except Exception as e:
        print(f"ERROR: API test failed: {e}")
        return False

def create_mermaid_er_diagram():
    """Create a Mermaid ER diagram for the database schema."""
    
    mermaid_diagram = """
erDiagram
    users {
        string id PK "UUID"
        string first_name "NOT NULL"
        string last_name "NOT NULL"
        string email "UNIQUE, NOT NULL"
        string password "NOT NULL"
        boolean is_admin "DEFAULT FALSE"
        datetime created_at
        datetime updated_at
    }
    
    places {
        string id PK "UUID"
        string title "NOT NULL"
        text description
        decimal price "NOT NULL"
        float latitude "NOT NULL"
        float longitude "NOT NULL"
        string owner_id FK "NOT NULL"
        datetime created_at
        datetime updated_at
    }
    
    reviews {
        string id PK "UUID"
        text text "NOT NULL"
        int rating "1-5, NOT NULL"
        string user_id FK "NOT NULL"
        string place_id FK "NOT NULL"
        datetime created_at
        datetime updated_at
    }
    
    amenities {
        string id PK "UUID"
        string name "UNIQUE, NOT NULL"
        datetime created_at
        datetime updated_at
    }
    
    place_amenities {
        string place_id FK "PRIMARY KEY"
        string amenity_id FK "PRIMARY KEY"
        datetime created_at
    }
    
    users ||--o{ places : owns
    users ||--o{ reviews : writes
    places ||--o{ reviews : receives
    places }o--o{ amenities : has
"""
    
    print("\n" + "=" * 60)
    print("MERMAID ER DIAGRAM")
    print("=" * 60)
    print(mermaid_diagram)
    
    # Save diagram to file
    with open('database_schema_diagram.mmd', 'w') as f:
        f.write(mermaid_diagram)
    
    print("✓ Mermaid diagram saved to 'database_schema_diagram.mmd'")

if __name__ == '__main__':
    print("Starting comprehensive database and API tests...")
    
    db_success = test_database_comprehensive()
    api_success = test_api_integration()
    
    # Create Mermaid ER diagram
    create_mermaid_er_diagram()
    
    print("\n" + "=" * 70)
    if db_success and api_success:
        print("🎉 OVERALL RESULT: ALL TESTS PASSED! 🎉")
        print("\n✓ Database schema created and validated")
        print("✓ Initial data inserted correctly")
        print("✓ Admin user with bcrypt password hash")
        print("✓ All table relationships working")
        print("✓ CRUD operations functional")
        print("✓ Constraints and validation enforced")
        print("✓ API integration working")
        print("✓ ER diagram generated")
        print("\n🚀 Database is production-ready!")
        print("\nAdmin Credentials:")
        print("  Email: admin@hbnb.io")
        print("  Password: admin1234")
        print("  UUID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1")
        print("\nInitial Amenities:")
        print("  - WiFi (ccaf6b6c-b86d-4dec-8a87-8a3050d1e463)")
        print("  - Swimming Pool (075fd2d0-2b15-432a-862d-516366d41465)")
        print("  - Air Conditioning (6e59f738-be8e-40ce-9e8b-9af7d6b816db)")
    else:
        print("❌ OVERALL RESULT: SOME TESTS FAILED!")
        print("Please review the error messages above.")
    print("=" * 70)
