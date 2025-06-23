from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Test User creation
def test_user_creation():
    user = User(first_name="John", last_name="Doe",
                email="john.doe@example.com", password="pwd123")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert hasattr(user, 'places') and isinstance(user.places, list)
    print("√ User creation test passed!")

# Test Amenity creation
def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("√ Amenity creation test passed!")

# Test Place and Review relationships
def test_place_creation_and_relationships():
    owner = User(first_name="Alice", last_name="Smith",
                 email="alice@example.com")
    place = Place(name="Ocean View",
                  description="Nice place by the beach", price=200,
                  latitude=25.7617, longitude=-80.1918, owner=owner)

    # Test place properties
    assert place.name == "Ocean View"
    assert place.owner == owner
    assert place.reviews == []
    assert place.amenities == []

    # Add review
    review = Review(user=owner, place=place, rating=4, comment="Great view!")
    place.add_reviews(review)
    assert len(place.reviews) == 1
    assert place.reviews[0].comment == "Great view!"

    # Add amenities
    wifi = Amenity(name="Wi-Fi")
    pool = Amenity(name="Pool")
    place.add_amenity(wifi)
    place.add_amenity(pool)
    assert wifi in place.amenities
    assert pool in place.amenities

    print("√ Place creation and relationships test passed!")

# Run all tests
if __name__ == "__main__":
    test_user_creation()
    test_amenity_creation()
    test_place_creation_and_relationships()
