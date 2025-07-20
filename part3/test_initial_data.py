#!/usr/bin/env python3
"""
Test script to verify that the initial data works correctly with the Flask application.
This script tests the integration between the database initial data and the application.
"""

from app import create_app, db
from app.models.user import User
from app.models.amenities import Amenity

def test_initial_data_integration():
    """Test that the initial data integrates correctly with the application."""
    
    print("Testing Initial Data Integration with Flask Application")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Test 1: Check if admin user exists and can be retrieved
            print("\n1. Testing Admin User Integration...")
            admin_user = User.query.filter_by(email='admin@hbnb.io').first()
            
            if admin_user:
                print(f"   Admin user found: {admin_user.email}")
                print(f"   Name: {admin_user.first_name} {admin_user.last_name}")
                print(f"   Admin status: {admin_user.is_admin}")
                print(f"   User ID: {admin_user.id}")
                
                # Test password verification
                is_password_correct = admin_user.verify_password('admin1234')
                print(f"   Password verification: {'PASS' if is_password_correct else 'FAIL'}")
            else:
                print("   ERROR: Admin user not found!")
                return False
            
            # Test 2: Check if initial amenities exist
            print("\n2. Testing Initial Amenities Integration...")
            required_amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']
            found_amenities = []
            
            for amenity_name in required_amenities:
                amenity = Amenity.query.filter_by(name=amenity_name).first()
                if amenity:
                    found_amenities.append(amenity_name)
                    print(f"   Found: {amenity.name} (ID: {amenity.id})")
                else:
                    print(f"   ERROR: {amenity_name} not found!")
            
            if len(found_amenities) != len(required_amenities):
                print(f"   ERROR: Expected {len(required_amenities)} amenities, found {len(found_amenities)}")
                return False
            
            # Test 3: Test authentication through facade
            print("\n3. Testing Authentication through Facade...")
            from app.services import facade
            
            authenticated_user = facade.authenticate_user('admin@hbnb.io', 'admin1234')
            if authenticated_user:
                print("   Authentication successful through facade")
                print(f"   Authenticated user: {authenticated_user.email}")
            else:
                print("   ERROR: Authentication failed through facade")
                return False
            
            # Test 4: Test wrong password rejection
            print("\n4. Testing Wrong Password Rejection...")
            wrong_auth = facade.authenticate_user('admin@hbnb.io', 'wrongpassword')
            if not wrong_auth:
                print("   Wrong password correctly rejected")
            else:
                print("   ERROR: Wrong password was accepted!")
                return False
            
            # Test 5: Test getting user by email
            print("\n5. Testing User Retrieval by Email...")
            user_by_email = facade.get_user_by_email('admin@hbnb.io')
            if user_by_email and user_by_email.id == admin_user.id:
                print("   User retrieval by email successful")
            else:
                print("   ERROR: User retrieval by email failed")
                return False
            
            # Test 6: Test amenities retrieval
            print("\n6. Testing Amenities Retrieval...")
            all_amenities = facade.get_all_amenities()
            amenity_names = [a.name for a in all_amenities]
            
            for required_amenity in required_amenities:
                if required_amenity in amenity_names:
                    print(f"   Amenity '{required_amenity}' accessible through facade")
                else:
                    print(f"   ERROR: Amenity '{required_amenity}' not accessible through facade")
                    return False
            
            print("\n" + "=" * 70)
            print("SUCCESS: All initial data integration tests passed!")
            print("\nInitial Data Summary:")
            print("- Admin user created and accessible")
            print("- Password authentication working")
            print("- All required amenities present")
            print("- Facade methods working correctly")
            print("\nYou can now login to the application with:")
            print("Email: admin@hbnb.io")
            print("Password: admin1234")
            
            return True
            
        except Exception as e:
            print(f"\nERROR: Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_api_authentication():
    """Test authentication through API endpoints."""
    
    print("\n" + "=" * 70)
    print("Testing API Authentication with Initial Data")
    print("=" * 70)
    
    try:
        app = create_app()
        
        with app.test_client() as client:
            # Test login endpoint
            login_data = {
                'email': 'admin@hbnb.io',
                'password': 'admin1234'
            }
            
            response = client.post('/api/v1/auth/login', 
                                   json=login_data,
                                   content_type='application/json')
            
            if response.status_code == 200:
                data = response.get_json()
                if 'access_token' in data:
                    print("API authentication successful!")
                    print("Access token generated successfully")
                    return True
                else:
                    print("ERROR: No access token in response")
                    return False
            else:
                print(f"ERROR: Login failed with status code {response.status_code}")
                print(f"Response: {response.get_json()}")
                return False
                
    except Exception as e:
        print(f"ERROR: API test failed with exception: {e}")
        return False

if __name__ == '__main__':
    success1 = test_initial_data_integration()
    success2 = test_api_authentication()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("OVERALL STATUS: ALL TESTS PASSED")
        print("Initial data is properly integrated and working!")
    else:
        print("OVERALL STATUS: SOME TESTS FAILED")
        print("Please check the error messages above.")
    print("=" * 70)
