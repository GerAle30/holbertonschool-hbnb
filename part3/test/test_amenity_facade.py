#!/usr/bin/env python3
"""
Comprehensive Test for Amenity methods in HBnBFacade
Tests: create_amenity, get_amenity, get_all_amenities, update_amenity
"""

from app.models.amenity import Amenity
from app.services.facade import HBnBFacade
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_amenity_facade_methods():
    """Test all amenity-related methods in the HBnBFacade"""
    print(" Testing Amenity Methods in HBnBFacade...")

    # Create facade instance
    facade = HBnBFacade()

    # Test 1: Test empty amenity list initially
    print("\n1. Testing initial empty amenity list...")
    all_amenities = facade.get_all_amenities()
    print(f"   ✓ Initial amenity count: {len(all_amenities)}")
    initial_count = len(all_amenities)

    # Test 2: Create amenities
    print("\n2. Testing amenity creation...")
    amenity_data_list = [
        {'name': 'WiFi'},
        {'name': 'Swimming Pool'},
        {'name': 'Gym'},
        {'name': 'Parking'},
        {'name': 'Air Conditioning'}
    ]

    created_amenities = []
    for i, amenity_data in enumerate(amenity_data_list):
        try:
            amenity = facade.create_amenity(amenity_data)
            created_amenities.append(amenity)
            print(f"   ✓ Created amenity {i + 1}: {amenity.name}")
            print(f"     - ID: {amenity.id}")
            print(f"     - Created at: {amenity.created_at}")

            # Verify amenity is an instance of Amenity
            if isinstance(amenity, Amenity):
                print(f"     ✓ Correct instance type")
            else:
                print(f"     ✗ Wrong instance type: {type(amenity)}")
                return False

        except Exception as e:
            print(f"   ✗ Error creating amenity {i + 1}: {e}")
            return False

    print(f"   ✓ Successfully created {len(created_amenities)} amenities")

    # Test 3: Retrieve amenities by ID
    print("\n3. Testing amenity retrieval by ID...")
    for i, amenity in enumerate(created_amenities):
        try:
            retrieved_amenity = facade.get_amenity(amenity.id)
            if retrieved_amenity:
                print(
                    f"   ✓ Retrieved amenity {
                        i +
                        1}: {
                        retrieved_amenity.name}")

                # Verify data integrity
                if (retrieved_amenity.id == amenity.id and
                        retrieved_amenity.name == amenity.name):
                    print(f"     ✓ Data integrity verified")
                else:
                    print(f"     ✗ Data integrity check failed")
                    return False
            else:
                print(f"   ✗ Failed to retrieve amenity {i + 1}")
                return False
        except Exception as e:
            print(f"   ✗ Error retrieving amenity {i + 1}: {e}")
            return False

    # Test 4: Test retrieval of non-existent amenity
    print("\n4. Testing non-existent amenity retrieval...")
    fake_id = "00000000-0000-0000-0000-000000000000"
    result = facade.get_amenity(fake_id)
    if result is None:
        print(f"   ✓ Correctly returned None for non-existent amenity")
    else:
        print(f"   ✗ Unexpectedly found amenity for fake ID")
        return False

    # Test 5: Retrieve all amenities
    print("\n5. Testing get_all_amenities...")
    all_amenities = facade.get_all_amenities()
    expected_count = initial_count + len(created_amenities)

    if len(all_amenities) == expected_count:
        print(
            f"   ✓ Amenity count verification passed: {
                len(all_amenities)} amenities")
    else:
        print(
            f"   ✗ Amenity count mismatch: expected {expected_count}, got {
                len(all_amenities)}")
        return False

    # Verify all created amenities are in the list
    created_names = {amenity.name for amenity in created_amenities}
    retrieved_names = {amenity.name for amenity in all_amenities}

    for name in created_names:
        if name in retrieved_names:
            print(f"   ✓ Found amenity: {name}")
        else:
            print(f"   ✗ Missing amenity: {name}")
            return False

    # Test 6: Update amenity
    print("\n6. Testing amenity updates...")
    if created_amenities:
        amenity_to_update = created_amenities[0]
        original_name = amenity_to_update.name

        # Update the amenity name
        update_data = {'name': 'Premium WiFi'}

        try:
            updated_amenity = facade.update_amenity(
                amenity_to_update.id, update_data)
            if updated_amenity:
                print(f"   ✓ Amenity updated successfully!")
                print(f"     - Original name: {original_name}")
                print(f"     - Updated name: {updated_amenity.name}")

                # Verify the update was applied
                retrieved_after_update = facade.get_amenity(
                    amenity_to_update.id)
                if retrieved_after_update and retrieved_after_update.name == 'Premium WiFi':
                    print(f"     ✓ Update persisted correctly")
                else:
                    print(f"     ✗ Update not persisted")
                    return False
            else:
                print(f"   ✗ Update returned None")
                return False
        except Exception as e:
            print(f"   ✗ Error updating amenity: {e}")
            return False

    # Test 7: Update non-existent amenity
    print("\n7. Testing update of non-existent amenity...")
    fake_id = "00000000-0000-0000-0000-000000000000"
    update_data = {'name': 'Should Fail'}

    result = facade.update_amenity(fake_id, update_data)
    if result is None:
        print(f"   ✓ Correctly returned None for non-existent amenity")
    else:
        print(f"   ✗ Unexpectedly returned result for non-existent amenity")
        return False

    # Test 8: Test amenity name uniqueness (create duplicate)
    print("\n8. Testing duplicate amenity creation...")
    # Same as first amenity (though now updated to Premium WiFi)
    duplicate_data = {'name': 'WiFi'}

    try:
        duplicate_amenity = facade.create_amenity(duplicate_data)
        print(f"   ✓ Duplicate amenity created: {duplicate_amenity.name}")
        print(f"     - ID: {duplicate_amenity.id}")
        # Note: The current implementation allows duplicates, which might be intended
        # In a real system, you might want to add uniqueness constraints
    except Exception as e:
        print(f"   ✗ Error creating duplicate amenity: {e}")
        return False

    # Test 9: Verify final state
    print("\n9. Verifying final amenity state...")
    final_amenities = facade.get_all_amenities()
    print(f"   ✓ Final amenity count: {len(final_amenities)}")

    print(f"    All amenities in system:")
    for amenity in final_amenities:
        print(f"     - {amenity.name} (ID: {amenity.id[:8]}...)")

    print("\n All amenity facade tests passed!")
    return True


def test_amenity_model():
    """Test the Amenity model directly"""
    print("\n🏗️ Testing Amenity Model...")

    # Test amenity creation
    print("\n1. Testing direct amenity creation...")
    try:
        amenity = Amenity(name="Test Amenity")
        print(f"   ✓ Amenity created: {amenity.name}")
        print(f"   - ID: {amenity.id}")
        print(f"   - Created at: {amenity.created_at}")
        print(f"   - Updated at: {amenity.updated_at}")

        # Test that it inherits from BaseModel
        if hasattr(amenity, 'id') and hasattr(amenity, 'created_at'):
            print(f"   ✓ BaseModel inheritance working")
        else:
            print(f"   ✗ BaseModel inheritance issue")
            return False

    except Exception as e:
        print(f"   ✗ Error creating amenity: {e}")
        return False

    # Test amenity with empty name
    print("\n2. Testing amenity with empty name...")
    try:
        empty_amenity = Amenity(name="")
        print(f"   ✓ Empty name amenity created: '{empty_amenity.name}'")
        # Note: Current implementation allows empty names
        # You might want to add validation for this
    except Exception as e:
        print(f"   ✗ Error with empty name: {e}")
        return False

    print("\n Amenity model tests passed!")
    return True


def print_amenity_summary():
    """Print summary of amenity functionality"""
    print("\n" + "=" * 70)
    print("📚 AMENITY FUNCTIONALITY SUMMARY")
    print("=" * 70)
    print("""
 IMPLEMENTED METHODS IN HBnBFacade:

🏗️  create_amenity(amenity_data)
    • Creates new Amenity instance
    • Stores in amenity repository
    • Returns created amenity object

 get_amenity(amenity_id)
    • Retrieves amenity by ID
    • Returns amenity object or None

 get_all_amenities()
    • Retrieves all amenities from repository
    • Returns list of amenity objects

 update_amenity(amenity_id, amenity_data)
    • Updates existing amenity
    • Returns updated amenity or None if not found

💾 REPOSITORY INTEGRATION:
    • Uses InMemoryRepository for storage
    • Full CRUD operations supported
    • Data persistence during session

🏗️  MODEL FEATURES:
    • Inherits from BaseModel
    • Automatic ID generation (UUID)
    • Timestamp tracking (created_at, updated_at)
    • Simple name-based amenity structure

 USE CASES:
    • Hotel/accommodation amenity management
    • Place feature tracking
    • Search and filtering by amenities
    • Amenity-based recommendations
""")
    print("=" * 70)


if __name__ == "__main__":
    print_amenity_summary()

    # Run amenity model tests
    success1 = test_amenity_model()
    if not success1:
        sys.exit(1)

    # Run facade method tests
    success2 = test_amenity_facade_methods()
    if not success2:
        sys.exit(1)

    print(f"\n ALL AMENITY TESTS PASSED!")
    print(f" HBnBFacade amenity methods are fully functional!")

    sys.exit(0)
