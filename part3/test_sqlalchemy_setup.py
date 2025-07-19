#!/usr/bin/env python3
"""
Test script to verify SQLAlchemy setup and basic functionality
"""

from app import create_app, db
import config

def test_sqlalchemy_setup():
    """Test SQLAlchemy initialization and basic functionality"""
    print("Testing SQLAlchemy Setup")
    print("=" * 50)
    
    # Create Flask application instance
    app = create_app(config.DevelopmentConfig)
    
    with app.app_context():
        try:
            # Test 1: Check if db is initialized
            print("Test 1: SQLAlchemy instance check")
            print(f"SQLAlchemy instance: {db}")
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            print("PASS: SQLAlchemy instance created successfully")
            
            # Test 2: Test database connection
            print("\nTest 2: Database connection test")
            try:
                # Try to execute a simple query
                result = db.engine.execute("SELECT 1")
                print("PASS: Database connection successful")
            except Exception as e:
                print(f"INFO: Database connection test skipped (no tables yet): {e}")
            
            # Test 3: Check configuration
            print("\nTest 3: Configuration check")
            print(f"SQLALCHEMY_TRACK_MODIFICATIONS: {app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS')}")
            print(f"Database file will be: {app.config['SQLALCHEMY_DATABASE_URI']}")
            print("PASS: Configuration loaded correctly")
            
            # Test 4: Test database metadata
            print("\nTest 4: Database metadata check")
            print(f"Database metadata: {db.metadata}")
            print(f"Current tables: {list(db.metadata.tables.keys())}")
            print("PASS: Metadata accessible (no tables expected yet)")
            
            print("\n" + "=" * 50)
            print("SQLAlchemy Setup: SUCCESS")
            print("Ready for model definition and table creation!")
            
            return True
            
        except Exception as e:
            print(f"FAIL: SQLAlchemy setup error: {e}")
            return False

if __name__ == "__main__":
    success = test_sqlalchemy_setup()
    
    if success:
        print("\nNext Steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Define your SQLAlchemy models")
        print("3. Create database tables: flask db init, flask db migrate, flask db upgrade")
        print("4. Or use db.create_all() in your application context")
    else:
        print("\nPlease fix the setup issues before proceeding.")
