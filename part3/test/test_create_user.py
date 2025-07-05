#!/usr/bin/env python3
"""
Test script for Create User endpoint (POST /api/v1/users/)
"""

from app.models.user import User
from app.services.facade import HBnBFacade
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_create_user():
    """Test the user creation functionality"""
    print("Testing Create User (POST /api/v1/users/)...")

    # Create facade instance
    facade = HBnBFacade()

    # Test 1: Create a valid user
    print("\n1. Creating a valid user...")
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice.johnson@example.com'
    }

    try:
        created_user = facade.create_user(user_data)
        print(f"   ✓ User created successfully!")
        print(f"   - ID: {created_user.id}")
        print(f"   - Name: {created_user.first_name} {created_user.last_name}")
        print(f"   - Email: {created_user.email}")
        print(f"   - Is Admin: {created_user.is_admin}")
        print(f"   - Created at: {created_user.created_at}")
        print(f"   - Updated at: {created_user.updated_at}")
    except Exception as e:
        print(f"   ✗ Error creating user: {e}")
        return False

    # Test 2: Try to create user with duplicate email
    print("\n2. Testing duplicate email handling...")
    duplicate_user_data = {
        'first_name': 'Bob',
        'last_name': 'Smith',
        'email': 'alice.johnson@example.com'  # Same email as above
    }

    try:
        # Check if email already exists
        existing_user = facade.get_user_by_email(duplicate_user_data['email'])
        if existing_user:
            print("   ✓ Correctly detected duplicate email")
        else:
            print("   ✗ Failed to detect duplicate email")
            return False
    except Exception as e:
        print(f"   ✗ Error checking duplicate email: {e}")
        return False

    # Test 3: Create user with different valid data
    print("\n3. Creating another valid user...")
    user_data_2 = {
        'first_name': 'Charlie',
        'last_name': 'Brown',
        'email': 'charlie.brown@example.com'
    }

    try:
        created_user_2 = facade.create_user(user_data_2)
        print(f"   ✓ Second user created successfully!")
        print(f"   - ID: {created_user_2.id}")
        print(
            f"   - Name: {created_user_2.first_name} {created_user_2.last_name}")
        print(f"   - Email: {created_user_2.email}")
    except Exception as e:
        print(f"   ✗ Error creating second user: {e}")
        return False

    # Test 4: Test invalid data handling
    print("\n4. Testing invalid data handling...")

    # Test empty first name
    try:
        invalid_data = {
            'first_name': '',
            'last_name': 'Test',
            'email': 'test@example.com'
        }
        facade.create_user(invalid_data)
        print("   ✗ Should have failed with empty first name")
        return False
    except ValueError as e:
        print(f"   ✓ Correctly rejected empty first name: {e}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

    # Test invalid email
    try:
        invalid_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid-email'
        }
        facade.create_user(invalid_data)
        print("   ✗ Should have failed with invalid email")
        return False
    except ValueError as e:
        print(f"   ✓ Correctly rejected invalid email: {e}")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

    # Test 5: Verify all users can be retrieved
    print("\n5. Verifying all users can be retrieved...")
    try:
        all_users = facade.get_all_users()
        print(f"   ✓ Retrieved {len(all_users)} users total")
        for user in all_users:
            print(f"     - {user.first_name} {user.last_name} ({user.email})")
    except Exception as e:
        print(f"   ✗ Error retrieving all users: {e}")
        return False

    # Test 6: Test data integrity
    print("\n6. Testing data integrity...")
    if (created_user.first_name == user_data['first_name'] and
        created_user.last_name == user_data['last_name'] and
        created_user.email == user_data['email'] and
            created_user.is_admin is False):  # Default value
        print("   ✓ All user data integrity checks passed")
    else:
        print("   ✗ User data integrity check failed")
        return False

    print("\n🎉 All tests passed! Create User endpoint is working correctly.")
    return True


if __name__ == "__main__":
    success = test_create_user()
    sys.exit(0 if success else 1)
