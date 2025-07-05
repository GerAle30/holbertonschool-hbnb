#!/usr/bin/env python3
"""
Test script to demonstrate password hashing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.user import User

def test_password_hashing():
    """Test password hashing functionality directly"""
    print("=== Testing Password Hashing Functionality ===\n")
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Test 1: Create a user and hash password
        print("1. Testing User Creation with Password Hashing:")
        print("-" * 50)
        
        try:
            user = User("John", "Doe", "john@example.com")
            print(f"Created user: {user.first_name} {user.last_name}")
            print(f"Email: {user.email}")
            print(f"Initial password value: {user.password}")
            
            # Hash a password
            test_password = "mySecurePassword123"
            user.hash_password(test_password)
            print(f"After hashing password '{test_password}':")
            print(f"Hashed password: {user.password}")
            print(f"Password starts with bcrypt hash: {user.password.startswith('$2b$')}")
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return
        
        print("\n2. Testing Password Verification:")
        print("-" * 50)
        
        # Test correct password
        is_correct = user.verify_password(test_password)
        print(f"Verifying correct password '{test_password}': {is_correct}")
        
        # Test incorrect password
        wrong_password = "wrongPassword"
        is_wrong = user.verify_password(wrong_password)
        print(f"Verifying wrong password '{wrong_password}': {is_wrong}")
        
        print("\n3. Testing User Data Exposure:")
        print("-" * 50)
        
        # Simulate what would be returned by API
        user_response = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        
        print("API Response (password excluded):")
        for key, value in user_response.items():
            print(f"  {key}: {value}")
        
        print(f"\nPassword field excluded from response: {'password' not in user_response}")

if __name__ == "__main__":
    test_password_hashing()
