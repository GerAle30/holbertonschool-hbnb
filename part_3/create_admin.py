#!/usr/bin/env python3
"""Script to create an admin user"""

from app import create_app, db
from app.models.user import User

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@hbnb.com').first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User(
            first_name='Admin',
            last_name='User',
            email='admin@hbnb.com',
            password='admin123',
            is_admin=True
        )
        
        admin_user.save()
        print("Admin user created successfully!")
        print("Email: admin@hbnb.com")
        print("Password: admin123")

if __name__ == '__main__':
    create_admin_user()
