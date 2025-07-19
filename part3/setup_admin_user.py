#!/usr/bin/env python3
"""
Admin User Setup Utility
This script helps create an initial admin user to bootstrap the admin endpoint testing
"""

import os
import sys
import hashlib

def generate_sql_for_admin_user():
    """Generate SQL commands to create an admin user"""
    print("DATABASE DIRECT INSERT METHOD")
    print("="*50)
    
    # Generate a simple UUID (in production, use proper UUID generation)
    import uuid
    user_id = str(uuid.uuid4())
    
    # Simple password hashing (in production, use proper bcrypt/scrypt)
    password = "admin123"
    # This is a simplified hash - your app should use bcrypt
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    print("\nSQL Commands to create admin user:")
    print("="*50)
    
    # PostgreSQL version
    print("\n-- For PostgreSQL:")
    print(f"""
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '{user_id}',
    'System',
    'Administrator', 
    'admin@example.com',
    '{password_hash}',  -- Note: Use proper password hashing in production
    true,
    NOW(),
    NOW()
);
""")
    
    # SQLite version  
    print("\n-- For SQLite:")
    print(f"""
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '{user_id}',
    'System',
    'Administrator',
    'admin@example.com', 
    '{password_hash}',
    1,  -- SQLite uses 1 for true
    datetime('now'),
    datetime('now')
);
""")
    
    print(f"\nAdmin Credentials:")
    print(f"Email: admin@example.com")
    print(f"Password: {password}")
    print(f"User ID: {user_id}")
    
    return user_id, password

def generate_python_setup_code():
    """Generate Python code to auto-create admin user"""
    print("\n\nAPPLICATION CODE METHOD") 
    print("="*50)
    
    print("\nAdd this code to your app startup (e.g., in app/__init__.py or main):")
    print("="*50)
    
    setup_code = '''
def ensure_admin_user_exists():
    """Ensure at least one admin user exists in the system"""
    from app.services import facade
    
    admin_email = "admin@example.com"
    admin_password = "admin123"
    
    # Check if admin user already exists
    existing_admin = facade.get_user_by_email(admin_email)
    if existing_admin:
        print(f"Admin user already exists: {admin_email}")
        return existing_admin
    
    # Create admin user
    try:
        admin_user_data = {
            'first_name': 'System',
            'last_name': 'Administrator',
            'email': admin_email,
            'password': admin_password,
            'is_admin': True  # This is the key flag!
        }
        
        admin_user = facade.create_user(admin_user_data)
        print(f"Created admin user: {admin_email}")
        print(f"Password: {admin_password}")
        return admin_user
        
    except Exception as e:
        print(f"Failed to create admin user: {e}")
        return None

# Call this function when your app starts
if __name__ == "__main__":
    ensure_admin_user_exists()
'''
    
    print(setup_code)

def generate_environment_setup():
    """Generate environment variable setup"""
    print("\n\nENVIRONMENT VARIABLE METHOD")
    print("="*50)
    
    print("\nSet these environment variables:")
    print("="*30)
    
    env_setup = '''
# In your shell or .env file
export ADMIN_EMAIL="admin@example.com"
export ADMIN_PASSWORD="admin123"  
export AUTO_CREATE_ADMIN="true"
export FLASK_ENV="development"
'''
    
    print(env_setup)
    
    print("\nAdd this code to your application startup:")
    print("="*45)
    
    app_code = '''
import os
from app.services import facade

def setup_admin_from_env():
    """Create admin user from environment variables"""
    if os.getenv('AUTO_CREATE_ADMIN', 'false').lower() == 'true':
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        # Check if admin exists
        if not facade.get_user_by_email(admin_email):
            admin_data = {
                'first_name': 'Environment',
                'last_name': 'Admin',
                'email': admin_email,
                'password': admin_password,
                'is_admin': True
            }
            
            admin = facade.create_user(admin_data)
            print(f"Created admin from environment: {admin_email}")

# Call during app initialization  
setup_admin_from_env()
'''
    
    print(app_code)

def test_admin_connection():
    """Test if we can connect to an admin user"""
    print("\n\nTESTING EXISTING ADMIN CONNECTION")
    print("="*50)
    
    import requests
    
    BASE_URL = "http://127.0.0.1:5000/api/v1"
    
    # Test common admin credentials
    test_credentials = [
        {"email": "admin@example.com", "password": "admin123"},
        {"email": "admin@example.com", "password": "adminpass123"},
        {"email": "admin@hbnb.io", "password": "admin123"},
        {"email": "root@example.com", "password": "rootpass123"},
        {"email": "system@example.com", "password": "system123"}
    ]
    
    print("\nTrying common admin credentials...")
    
    for i, creds in enumerate(test_credentials, 1):
        try:
            response = requests.post(f"{BASE_URL}/auth/login", json=creds, timeout=5)
            
            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get('access_token')
                
                # Verify admin status
                headers = {"Authorization": f"Bearer {token}"}
                protected_response = requests.get(f"{BASE_URL}/auth/protected", headers=headers)
                
                if protected_response.status_code == 200:
                    protected_data = protected_response.json()
                    is_admin = protected_data.get('is_admin', False)
                    
                    if is_admin:
                        print(f"Found working admin: {creds['email']}")
                        print(f"Password: {creds['password']}")
                        print(f"Token: {token[:30]}...")
                        return creds['email'], creds['password'], token
                    else:
                        print(f"{i}. {creds['email']}: Valid user but not admin")
                else:
                    print(f"{i}. {creds['email']}: Token verification failed")
            else:
                print(f"{i}. {creds['email']}: Login failed ({response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"{i}. {creds['email']}: Connection error - {e}")
            
    print("\nNo working admin credentials found")
    return None, None, None

def main():
    """Main setup function"""
    print("ADMIN USER SETUP UTILITY")
    print("="*70)
    
    print("\nThis utility helps you create an admin user for testing admin endpoints.")
    print("Choose the method that works best for your environment:\n")
    
    # First, test if admin already exists
    email, password, token = test_admin_connection()
    
    if token:
        print(f"\nGreat! You already have a working admin user.")
        print(f"You can now run the admin endpoint tests with these credentials.")
        
        # Run quick curl test
        print(f"\nQuick test curl command:")
        print(f'curl -X GET "http://127.0.0.1:5000/api/v1/auth/protected" \\')
        print(f'  -H "Authorization: Bearer {token}"')
        
        return
    
    print(f"\nNo working admin user found. Let's create one!")
    
    while True:
        print(f"\nChoose setup method:")
        print(f"1. Database Direct Insert (SQL)")
        print(f"2. Application Code Method (Python)")  
        print(f"3. Environment Variable Method")
        print(f"4. Test Connection Again")
        print(f"5. Exit")
        
        choice = input(f"\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            generate_sql_for_admin_user()
        elif choice == "2":  
            generate_python_setup_code()
        elif choice == "3":
            generate_environment_setup()
        elif choice == "4":
            test_admin_connection()
        elif choice == "5":
            print(f"\nGoodbye! Set up your admin user and run the tests when ready.")
            break
        else:
            print(f"Invalid choice. Please enter 1-5.")
            
        input(f"\nPress Enter to continue...")

if __name__ == "__main__":
    main()
