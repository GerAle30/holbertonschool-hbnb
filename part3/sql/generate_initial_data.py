#!/usr/bin/env python3
"""
Script to generate bcrypt hash and UUIDs for initial data insertion.
This script generates the required values for the admin user and amenities.
"""

import bcrypt
import uuid

def generate_bcrypt_hash(password, rounds=12):
    """Generate bcrypt hash for a password."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=rounds)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def generate_uuids(count):
    """Generate specified number of UUIDs."""
    return [str(uuid.uuid4()) for _ in range(count)]

def main():
    print("Generating Initial Data Values")
    print("=" * 50)
    
    # Generate bcrypt hash for admin password
    admin_password = "admin1234"
    admin_hash = generate_bcrypt_hash(admin_password)
    
    print(f"Admin Password: {admin_password}")
    print(f"Bcrypt Hash: {admin_hash}")
    print()
    
    # Generate UUIDs for amenities
    amenities = ["WiFi", "Swimming Pool", "Air Conditioning"]
    amenity_uuids = generate_uuids(len(amenities))
    
    print("Amenity UUIDs:")
    for amenity, uuid_val in zip(amenities, amenity_uuids):
        print(f"  {amenity}: {uuid_val}")
    
    print("\n" + "=" * 50)
    print("SQL INSERT Statements:")
    print("=" * 50)
    
    # Admin user insert
    print("\n-- Insert Administrator User")
    print("INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES")
    print(f"('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '{admin_hash}', TRUE);")
    
    # Amenities insert
    print("\n-- Insert Initial Amenities")
    print("INSERT INTO amenities (id, name) VALUES")
    for i, (amenity, uuid_val) in enumerate(zip(amenities, amenity_uuids)):
        comma = "," if i < len(amenities) - 1 else ";"
        print(f"('{uuid_val}', '{amenity}'){comma}")
    
    print("\n" + "=" * 50)
    print("Values generated successfully!")
    
    return {
        'admin_hash': admin_hash,
        'amenity_uuids': dict(zip(amenities, amenity_uuids))
    }

if __name__ == '__main__':
    main()
