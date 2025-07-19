#!/usr/bin/env python3
"""
Test script to verify database integration and user creation functionality.
This script will create a test user directly using the facade and repository.
"""

from app import create_app, db
from app.services.facade import HBnBFacade

def test_database_integration():
    """Test the database integration by creating and retrieving users."""
    
    app = create_app()
    
    with app.app_context():
        # Initialize the facade
        facade = HBnBFacade()
        
        print("🔍 Testing Database Integration")
        print("=" * 50)
        
        # Test 1: Create a test user
        print("\n1. Creating a test user...")
        try:
            test_user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'password': 'password123'
            }
            
            user = facade.create_user(test_user_data)
            print(f"✅ User created successfully!")
            print(f"   ID: {user.id}")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Email: {user.email}")
            print(f"   Admin: {user.is_admin}")
            print(f"   Created: {user.created_at}")
            
            # Save the user ID for later tests
            user_id = user.id
            
        except Exception as e:
            print(f"❌ Failed to create user: {e}")
            return
        
        # Test 2: Retrieve the user by ID
        print("\n2. Retrieving user by ID...")
        try:
            retrieved_user = facade.get_user(user_id)
            if retrieved_user:
                print(f"✅ User retrieved successfully!")
                print(f"   ID: {retrieved_user.id}")
                print(f"   Name: {retrieved_user.first_name} {retrieved_user.last_name}")
                print(f"   Email: {retrieved_user.email}")
            else:
                print("❌ User not found")
                
        except Exception as e:
            print(f"❌ Failed to retrieve user: {e}")
        
        # Test 3: Retrieve user by email
        print("\n3. Retrieving user by email...")
        try:
            email_user = facade.get_user_by_email('john.doe@example.com')
            if email_user:
                print(f"✅ User found by email!")
                print(f"   ID: {email_user.id}")
                print(f"   Email: {email_user.email}")
            else:
                print("❌ User not found by email")
                
        except Exception as e:
            print(f"❌ Failed to retrieve user by email: {e}")
        
        # Test 4: Test password verification
        print("\n4. Testing password verification...")
        try:
            if user.verify_password('password123'):
                print("✅ Password verification successful!")
            else:
                print("❌ Password verification failed")
                
        except Exception as e:
            print(f"❌ Password verification error: {e}")
        
        # Test 5: Get all users
        print("\n5. Getting all users...")
        try:
            all_users = facade.get_all_users()
            print(f"✅ Retrieved {len(all_users)} users from database")
            for user in all_users:
                print(f"   - {user.first_name} {user.last_name} ({user.email})")
                
        except Exception as e:
            print(f"❌ Failed to get all users: {e}")
        
        # Test 6: Test UserRepository specialized methods
        print("\n6. Testing UserRepository specialized methods...")
        try:
            # Test email exists
            exists = facade.user_repo.email_exists('john.doe@example.com')
            print(f"✅ Email exists check: {exists}")
            
            # Test user count
            count = facade.user_repo.count_users()
            print(f"✅ Total users: {count}")
            
            # Test admin count
            admin_count = facade.user_repo.count_admin_users()
            print(f"✅ Admin users: {admin_count}")
            
        except Exception as e:
            print(f"❌ Specialized methods error: {e}")
        
        # Test 7: Create an admin user for API testing
        print("\n7. Creating an admin user for API testing...")
        try:
            admin_data = {
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@example.com',
                'password': 'admin123',
                'is_admin': True
            }
            
            admin_user = facade.create_user(admin_data)
            print(f"✅ Admin user created successfully!")
            print(f"   ID: {admin_user.id}")
            print(f"   Email: {admin_user.email}")
            print(f"   Admin: {admin_user.is_admin}")
            
        except Exception as e:
            print(f"❌ Failed to create admin user: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Database integration test completed!")
        print("\nYou can now test the API endpoints:")
        print("1. Start the server: python3 run.py")
        print("2. Login as admin: POST /api/v1/auth/login")
        print("   Body: {'email': 'admin@example.com', 'password': 'admin123'}")
        print("3. Use the JWT token for authenticated requests")

if __name__ == '__main__':
    test_database_integration()
