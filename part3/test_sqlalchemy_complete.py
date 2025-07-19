#!/usr/bin/env python3
"""
Complete SQLAlchemy test with table creation and CRUD operations
This script verifies that SQLAlchemy is properly integrated and working
"""

from app import create_app, db
from app.models.example import ExampleModel
import config
import os


def test_complete_sqlalchemy():
    """Test complete SQLAlchemy functionality including CRUD operations"""
    print("Complete SQLAlchemy Test")
    print("=" * 60)
    
    # Create Flask application instance
    app = create_app(config.DevelopmentConfig)
    
    with app.app_context():
        try:
            # Test 1: Create database tables
            print("Test 1: Creating database tables")
            db.create_all()
            print(f"Database file created at: {app.instance_path}/hbnb_dev.db")
            print("PASS: Tables created successfully")
            
            # Test 2: Verify table creation
            print("\nTest 2: Verifying table creation")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Created tables: {tables}")
            if 'example' in tables:
                print("PASS: Example table created")
            else:
                print("FAIL: Example table not found")
                return False
            
            # Test 3: Test CREATE operation
            print("\nTest 3: Testing CREATE operation")
            example_record = ExampleModel(
                name="Test User",
                email="test@example.com"
            )
            db.session.add(example_record)
            db.session.commit()
            print(f"Created record: {example_record}")
            print("PASS: CREATE operation successful")
            
            # Test 4: Test READ operation
            print("\nTest 4: Testing READ operation")
            found_record = ExampleModel.query.filter_by(email="test@example.com").first()
            if found_record:
                print(f"Found record: {found_record.to_dict()}")
                print("PASS: READ operation successful")
            else:
                print("FAIL: Record not found")
                return False
            
            # Test 5: Test UPDATE operation
            print("\nTest 5: Testing UPDATE operation")
            found_record.name = "Updated Test User"
            db.session.commit()
            updated_record = ExampleModel.query.get(found_record.id)
            if updated_record.name == "Updated Test User":
                print(f"Updated record: {updated_record.to_dict()}")
                print("PASS: UPDATE operation successful")
            else:
                print("FAIL: UPDATE operation failed")
                return False
            
            # Test 6: Test DELETE operation
            print("\nTest 6: Testing DELETE operation")
            record_id = updated_record.id
            db.session.delete(updated_record)
            db.session.commit()
            deleted_check = ExampleModel.query.get(record_id)
            if deleted_check is None:
                print("PASS: DELETE operation successful")
            else:
                print("FAIL: DELETE operation failed")
                return False
            
            # Test 7: Test database constraints
            print("\nTest 7: Testing database constraints")
            try:
                # Try to create duplicate email (should fail)
                record1 = ExampleModel(name="User 1", email="duplicate@test.com")
                record2 = ExampleModel(name="User 2", email="duplicate@test.com")
                db.session.add(record1)
                db.session.commit()
                
                db.session.add(record2)
                db.session.commit()
                print("FAIL: Duplicate email constraint not enforced")
                return False
            except Exception as e:
                db.session.rollback()
                print(f"PASS: Unique constraint enforced - {type(e).__name__}")
            
            print("\n" + "=" * 60)
            print("Complete SQLAlchemy Test: SUCCESS")
            print("All CRUD operations and constraints working correctly!")
            
            return True
            
        except Exception as e:
            print(f"FAIL: SQLAlchemy test error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Clean up: Drop tables
            try:
                db.drop_all()
                print("\nCleanup: Test tables dropped")
            except:
                pass


def show_database_info():
    """Show information about the database setup"""
    app = create_app(config.DevelopmentConfig)
    
    print("\nDatabase Configuration:")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Track Modifications: {app.config['SQLALCHEMY_TRACK_MODIFICATIONS']}")
    print(f"Instance Path: {app.instance_path}")
    
    # Check if database file exists
    if 'sqlite:///' in app.config['SQLALCHEMY_DATABASE_URI']:
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not db_path.startswith('/'):
            db_path = os.path.join(app.instance_path, db_path)
        print(f"Database file path: {db_path}")
        print(f"Database exists: {os.path.exists(db_path)}")


if __name__ == "__main__":
    show_database_info()
    
    success = test_complete_sqlalchemy()
    
    if success:
        print("\nSQLAlchemy is fully set up and operational!")
        print("\nYou can now:")
        print("1. Define your actual models (User, Place, Review, etc.)")
        print("2. Use db.create_all() to create production tables")
        print("3. Use Flask-Migrate for database migrations")
        print("4. Implement your business logic with SQLAlchemy ORM")
    else:
        print("\nPlease fix the issues before proceeding with model development.")
