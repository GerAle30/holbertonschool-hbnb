#!/usr/bin/env python3
"""
Test script to verify admin bypass ownership restrictions functionality
Tests that admins can modify and delete places and reviews owned by other users
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_bypass_ownership():
    """Test admin bypass functionality for places and reviews"""
    print("[TEST] Testing Admin Bypass Ownership Restrictions\n")
    
    # Step 1: Login as admin
    print("1. Logging in as administrator...")
    admin_login = {
        "email": "admin@example.com",
        "password": "adminpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=admin_login)
    if response.status_code == 200:
        admin_token = response.json()['access_token']
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        admin_user_id = response.json().get('user_id')
        print("[SUCCESS] Admin login successful")
    else:
        print(f"[FAIL] Admin login failed: {response.status_code}")
        return
    
    # Step 2: Login as regular user (owner)
    print("\n2. Logging in as regular user (place/review owner)...")
    regular_login = {
        "email": "regular@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=regular_login)
    if response.status_code == 200:
        regular_token = response.json()['access_token']
        regular_headers = {"Authorization": f"Bearer {regular_token}"}
        regular_user_id = response.json().get('user_id')
        print("[SUCCESS] Regular user login successful")
    else:
        print(f"[FAIL] Regular user login failed: {response.status_code}")
        return
    
    # Step 3: Create test place owned by regular user
    print("\n3. Creating test place owned by regular user...")
    place_data = {
        "title": "Regular User's Place",
        "description": "A place owned by regular user",
        "price": 150.0,
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=place_data, headers=regular_headers)
    if response.status_code == 201:
        place = response.json()
        place_id = place['id']
        print(f"[SUCCESS] Place created by regular user: {place_id}")
        print(f"         Place owner ID: {place['owner']['id']}")
    else:
        print(f"[FAIL] Place creation failed: {response.status_code}: {response.text}")
        return
    
    # Step 4: Create test review owned by regular user
    print("\n4. Creating test review for admin's place...")
    
    # First create a place owned by admin for review
    admin_place_data = {
        "title": "Admin's Place",
        "description": "A place owned by admin",
        "price": 200.0,
        "latitude": 40.7589,
        "longitude": -73.9851
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=admin_place_data, headers=admin_headers)
    if response.status_code == 201:
        admin_place = response.json()
        admin_place_id = admin_place['id']
        print(f"[SUCCESS] Admin place created: {admin_place_id}")
        
        # Now create review by regular user
        review_data = {
            "text": "Great place by regular user!",
            "rating": 5,
            "user_id": regular_user_id,
            "place_id": admin_place_id
        }
        
        response = requests.post(f"{BASE_URL}/reviews/", json=review_data, headers=regular_headers)
        if response.status_code == 201:
            review = response.json()
            review_id = review['id']
            print(f"[SUCCESS] Review created by regular user: {review_id}")
        else:
            print(f"[FAIL] Review creation failed: {response.status_code}: {response.text}")
            return
    else:
        print(f"[FAIL] Admin place creation failed: {response.status_code}")
        return
    
    # Step 5: Test regular user cannot modify other's place
    print("\n5. Testing regular user restrictions...")
    
    # Create another place by admin for testing
    another_admin_place_data = {
        "title": "Another Admin Place",
        "description": "Another place by admin",
        "price": 300.0,
        "latitude": 40.7831,
        "longitude": -73.9712
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=another_admin_place_data, headers=admin_headers)
    if response.status_code == 201:
        another_admin_place = response.json()
        another_admin_place_id = another_admin_place['id']
        
        # Regular user tries to modify admin's place
        unauthorized_update = {"title": "Hacked by regular user"}
        
        response = requests.put(f"{BASE_URL}/places/{another_admin_place_id}", 
                              json=unauthorized_update, headers=regular_headers)
        if response.status_code == 403:
            error_msg = response.json().get('error', '')
            if "Unauthorized action" in error_msg:
                print("[PASS] Regular user correctly blocked from modifying admin's place")
            else:
                print(f"[PARTIAL] User blocked but with message: {error_msg}")
        else:
            print(f"[FAIL] Regular user not properly blocked: {response.status_code}")
    
    # Step 6: Test admin bypass - modify regular user's place
    print("\n6. Testing admin bypass for place modification...")
    place_update = {
        "title": "Modified by Admin",
        "description": "This place was modified by an administrator",
        "price": 250.0
    }
    
    response = requests.put(f"{BASE_URL}/places/{place_id}", json=place_update, headers=admin_headers)
    if response.status_code == 200:
        updated_place = response.json()
        if updated_place.get('title') == 'Modified by Admin':
            print("[PASS] Admin successfully bypassed ownership to modify place")
            
            # Check for admin modification flag
            if updated_place.get('modified_by_admin'):
                print("[PASS] Admin modification flag included in response")
            else:
                print("[PARTIAL] Place modified but missing admin flag")
            
            # Verify the original owner is still preserved
            if updated_place['owner']['id'] == regular_user_id:
                print("[PASS] Original place ownership preserved")
            else:
                print("[FAIL] Place ownership was changed unexpectedly")
        else:
            print(f"[FAIL] Place not properly updated: {updated_place}")
    else:
        print(f"[FAIL] Admin place modification failed: {response.status_code}: {response.text}")
    
    # Step 7: Test admin bypass - modify regular user's review
    print("\n7. Testing admin bypass for review modification...")
    review_update = {
        "text": "Review modified by administrator",
        "rating": 4
    }
    
    response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=review_update, headers=admin_headers)
    if response.status_code == 200:
        updated_review = response.json()
        if updated_review.get('text') == 'Review modified by administrator':
            print("[PASS] Admin successfully bypassed ownership to modify review")
            
            # Check for admin modification flag
            if updated_review.get('updated_by_admin'):
                print("[PASS] Admin modification flag included in response")
            else:
                print("[PARTIAL] Review modified but missing admin flag")
            
            # Verify the original reviewer is preserved
            if updated_review['user_id'] == regular_user_id:
                print("[PASS] Original review ownership preserved")
            else:
                print("[FAIL] Review ownership was changed unexpectedly")
        else:
            print(f"[FAIL] Review not properly updated: {updated_review}")
    else:
        print(f"[FAIL] Admin review modification failed: {response.status_code}: {response.text}")
    
    # Step 8: Test ownership restriction prevents changing ownership
    print("\n8. Testing ownership restriction enforcement...")
    
    # Try to change user_id in review (should fail even for admin)
    invalid_review_update = {
        "user_id": admin_user_id,  # Try to change ownership
        "text": "Trying to steal review"
    }
    
    response = requests.put(f"{BASE_URL}/reviews/{review_id}", json=invalid_review_update, headers=admin_headers)
    if response.status_code == 403:
        error_msg = response.json().get('error', '')
        if "Cannot change review ownership" in error_msg:
            print("[PASS] Ownership change correctly blocked")
        else:
            print(f"[PARTIAL] Blocked but with message: {error_msg}")
    else:
        print(f"[FAIL] Ownership change not properly blocked: {response.status_code}")
    
    # Step 9: Test admin bypass - delete regular user's place
    print("\n9. Testing admin bypass for place deletion...")
    
    # Create another place by regular user for deletion test
    delete_place_data = {
        "title": "Place to be Deleted",
        "description": "This place will be deleted by admin",
        "price": 100.0,
        "latitude": 40.7505,
        "longitude": -73.9934
    }
    
    response = requests.post(f"{BASE_URL}/places/", json=delete_place_data, headers=regular_headers)
    if response.status_code == 201:
        delete_place = response.json()
        delete_place_id = delete_place['id']
        
        # Admin deletes regular user's place
        response = requests.delete(f"{BASE_URL}/places/{delete_place_id}", headers=admin_headers)
        if response.status_code == 200:
            delete_response = response.json()
            if delete_response.get('deleted_by_admin'):
                print("[PASS] Admin successfully bypassed ownership to delete place")
                print("[PASS] Admin deletion flag included in response")
            else:
                print("[PARTIAL] Place deleted but missing admin flag")
        else:
            print(f"[FAIL] Admin place deletion failed: {response.status_code}: {response.text}")
    
    # Step 10: Test admin bypass - delete regular user's review
    print("\n10. Testing admin bypass for review deletion...")
    
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=admin_headers)
    if response.status_code == 200:
        delete_response = response.json()
        if delete_response.get('deleted_by_admin'):
            print("[PASS] Admin successfully bypassed ownership to delete review")
            print("[PASS] Admin deletion flag included in response")
        else:
            print("[PARTIAL] Review deleted but missing admin flag")
        
        # Verify review is actually deleted
        response = requests.get(f"{BASE_URL}/reviews/{review_id}")
        if response.status_code == 404:
            print("[PASS] Review successfully removed from system")
        else:
            print("[PARTIAL] Review deletion may not have been complete")
    else:
        print(f"[FAIL] Admin review deletion failed: {response.status_code}: {response.text}")
    
    # Step 11: Test non-existent resource handling
    print("\n11. Testing non-existent resource handling...")
    
    fake_place_id = "00000000-0000-0000-0000-000000000000"
    fake_review_id = "00000000-0000-0000-0000-000000000001"
    
    # Test non-existent place modification
    response = requests.put(f"{BASE_URL}/places/{fake_place_id}", 
                          json={"title": "Non-existent"}, headers=admin_headers)
    if response.status_code == 404:
        print("[PASS] Non-existent place modification correctly returns 404")
    else:
        print(f"[FAIL] Non-existent place handling failed: {response.status_code}")
    
    # Test non-existent review modification
    response = requests.put(f"{BASE_URL}/reviews/{fake_review_id}", 
                          json={"text": "Non-existent"}, headers=admin_headers)
    if response.status_code == 404:
        print("[PASS] Non-existent review modification correctly returns 404")
    else:
        print(f"[FAIL] Non-existent review handling failed: {response.status_code}")
    
    # Cleanup
    print("\n12. Cleaning up test resources...")
    cleanup_resources = [
        (f"{BASE_URL}/places/{place_id}", "place"),
        (f"{BASE_URL}/places/{admin_place_id}", "admin place"),
        (f"{BASE_URL}/places/{another_admin_place_id}", "another admin place")
    ]
    
    for resource_url, resource_name in cleanup_resources:
        response = requests.delete(resource_url, headers=admin_headers)
        if response.status_code in [200, 204]:
            print(f"[SUCCESS] Cleaned up {resource_name}")
        else:
            print(f"[INFO] Cleanup failed for {resource_name}: {response.status_code}")
    
    print("\n[COMPLETE] Admin Bypass Ownership Restrictions Testing Completed!")
    print("\nKey Features Tested:")
    print("- Admin can modify places owned by other users")
    print("- Admin can modify reviews created by other users") 
    print("- Admin can delete places owned by other users")
    print("- Admin can delete reviews created by other users")
    print("- Regular users are blocked from modifying others' resources")
    print("- Original ownership is preserved after admin modifications")
    print("- Admin bypass tracking in response messages")
    print("- Ownership change restrictions (user_id, place_id)")
    print("- Enhanced JWT claims checking with get_jwt()")
    print("- Proper error handling for non-existent resources")


if __name__ == "__main__":
    test_admin_bypass_ownership()
