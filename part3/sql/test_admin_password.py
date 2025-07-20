#!/usr/bin/env python3
"""
Test script to verify that the bcrypt hash works correctly for admin authentication.
This script tests the password verification process.
"""

import bcrypt

def test_password_verification():
    """Test that the generated bcrypt hash correctly verifies the admin password."""
    
    # Values from the insertion script
    admin_password = "admin1234"
    bcrypt_hash = "$2b$12$gcgR3rFYqYNWlyG.ntg1W.bV6LG.harP75KvOTIUnOXx8u5zhKZqS"
    
    print("Testing Admin Password Verification")
    print("=" * 50)
    print(f"Password: {admin_password}")
    print(f"Bcrypt Hash: {bcrypt_hash}")
    print()
    
    # Convert to bytes for bcrypt
    password_bytes = admin_password.encode('utf-8')
    hash_bytes = bcrypt_hash.encode('utf-8')
    
    # Test correct password
    is_valid = bcrypt.checkpw(password_bytes, hash_bytes)
    
    print("Verification Results:")
    print(f"Password '{admin_password}' matches hash: {is_valid}")
    
    if is_valid:
        print("✓ SUCCESS: Password verification works correctly")
    else:
        print("✗ FAILED: Password verification failed")
    
    # Test incorrect password
    wrong_password = "wrongpassword"
    wrong_password_bytes = wrong_password.encode('utf-8')
    is_invalid = bcrypt.checkpw(wrong_password_bytes, hash_bytes)
    
    print(f"Wrong password '{wrong_password}' matches hash: {is_invalid}")
    
    if not is_invalid:
        print("✓ SUCCESS: Wrong password correctly rejected")
    else:
        print("✗ FAILED: Wrong password was accepted")
    
    print()
    print("=" * 50)
    
    if is_valid and not is_invalid:
        print("Overall Status: ALL TESTS PASSED")
        print("The admin password hash is working correctly.")
    else:
        print("Overall Status: TESTS FAILED")
        print("There is an issue with the password hash.")
    
    return is_valid and not is_invalid

def simulate_application_auth():
    """Simulate how the application would authenticate the admin user."""
    
    print("\nSimulating Application Authentication")
    print("-" * 40)
    
    # Simulate database values
    stored_hash = "$2b$12$gcgR3rFYqYNWlyG.ntg1W.bV6LG.harP75KvOTIUnOXx8u5zhKZqS"
    
    # Simulate login attempts
    test_cases = [
        ("admin@hbnb.io", "admin1234", True),   # Correct credentials
        ("admin@hbnb.io", "wrongpass", False),  # Wrong password
        ("admin@hbnb.io", "Admin1234", False),  # Case sensitive
        ("admin@hbnb.io", "", False),           # Empty password
    ]
    
    for email, password, expected in test_cases:
        if password:
            result = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        else:
            result = False
        
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status} Login: {email} / {password} -> {result}")

if __name__ == '__main__':
    success = test_password_verification()
    simulate_application_auth()
    
    if success:
        print("\nThe admin user can be authenticated with:")
        print("Email: admin@hbnb.io")
        print("Password: admin1234")
    else:
        print("\nThere is an issue with the password configuration.")
