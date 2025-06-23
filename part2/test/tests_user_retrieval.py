#!/usr/bin/env python3
"""
Test script for User Retrieval by ID endpoint (GET /api/v1/users/<user_id>)
"""

from app.models.user import User
from app.services.facade import HBnBFacade
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_user_retrieval():
    """Test the user retrieval by ID functionality"""
    print("Testing User Retrieval by ID...")

    # Create facade instance
    facade = HBnBFacade()

    # Test 1: Create a test user
    print("\n1. Creating a test user...")
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'is_admin': False
    }

    try:
        created_user = facade.create_user(user_data)
        print(f"   ✓ User created successfully with ID: {created_user.id}")
        print(f"   - Name: {created_user.first_name} {created_user.last_name}")
        print(f"   - Email: {created_user.email}")
    except Exception as e:
        print(f"   ✗ Error creating user: {e}")
        return False

    # Test 2: Retrieve the user by ID
    print(f"\n2. Retrieving user by ID: {created_user.id}")
    try:
        retrieved_user = facade.get_user(created_user.id)
        if retrieved_user:
            print("   ✓ User retrieved successfully!")
            print(f"   - ID: {retrieved_user.id}")
            print(
                f"   - Name: {retrieved_user.first_name} {retrieved_user.last_name}")
            print(f"   - Email: {retrieved_user.email}")
            print(f"   - Created at: {retrieved_user.created_at}")
            print(f"   - Updated at: {retrieved_user.updated_at}")
        else:
            print("   ✗ User not found")
            return False
    except Exception as e:
        print(f"   ✗ Error retrieving user: {e}")
        return False

    # Test 3: Try to retrieve non-existent user
    print("\n3. Testing retrieval of non-existent user...")
    try:
        non_existent_user = facade.get_user("non-existent-id")
        if non_existent_user is None:
            print("   ✓ Correctly returned None for non-existent user")
        else:
            print("   ✗ Unexpectedly found a user")
            return False
    except Exception as e:
        print(f"   ✗ Error testing non-existent user: {e}")
        return False

    # Test 4: Verify user data matches
    print("\n4. Verifying data integrity...")
    if (retrieved_user.id == created_user.id and
        retrieved_user.first_name == created_user.first_name and
        retrieved_user.last_name == created_user.last_name and
            retrieved_user.email == created_user.email):
        print("   ✓ All user data matches correctly")
    else:
        print("   ✗ User data mismatch detected")
        return False

    print("\n🎉 All tests passed! User Retrieval by ID is working correctly.")
    return True


if __name__ == "__main__":
    success = test_user_retrieval()
    sys.exit(0 if success else ])
