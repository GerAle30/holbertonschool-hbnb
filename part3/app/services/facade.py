from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenities import Amenity
from app.models.place import Place
from app.models.reviews import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()  # Use specialized UserRepository
        self.place_repo = PlaceRepository()  # Use specialized PlaceRepository
        self.review_repo = ReviewRepository()  # Use specialized ReviewRepository
        self.amenity_repo = AmenityRepository()  # Use specialized AmenityRepository

    def create_user(self, user_data):
        """Create new user and store in the repo."""
        # Check if email already exists using UserRepository method
        if self.user_repo.email_exists(user_data.get('email')):
            raise ValueError("Email already registered")
        
        # Extract password from user_data to handle separately
        user_data_copy = user_data.copy()
        password = user_data_copy.pop('password', None)
        
        if not password:
            raise ValueError("Password is required")
        
        # Create user without password
        user = User(**user_data_copy)
        
        # Hash password
        user.hash_password(password)
        
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by id."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find user by email."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        # Handle password update using UserRepository specialized method
        if 'password' in user_data:
            password = user_data.pop('password')
            updated_user = self.user_repo.update_password(user_id, password)
            if not updated_user:
                return None
            # Continue with other updates if there are any
            if not user_data:  # If only password was being updated
                return updated_user
        
        # Check email uniqueness if email is being updated
        if 'email' in user_data:
            current_user = self.user_repo.get(user_id)
            if not current_user:
                return None
            
            new_email = user_data['email']
            if new_email != current_user.email and self.user_repo.email_exists(new_email):
                raise ValueError("Email already registered")
        
        # Update other fields using repository method
        return self.user_repo.update(user_id, user_data)
    
    def authenticate_user(self, email, password):
        """Authenticate a user with email and password."""
        return self.user_repo.authenticate_user(email, password)
    
    def get_users_by_name(self, first_name=None, last_name=None):
        """Search users by name."""
        return self.user_repo.get_users_by_name(first_name, last_name)
    
    def get_all_admin_users(self):
        """Retrieve all admin users."""
        return self.user_repo.get_all_admins()
    
    def toggle_user_admin_status(self, user_id):
        """Toggle admin status for a user."""
        return self.user_repo.toggle_admin_status(user_id)
    
    def get_recent_users(self, limit=10):
        """Get recently created users."""
        return self.user_repo.get_recent_users(limit)
    
    def get_user_statistics(self):
        """Get user statistics for admin dashboard."""
        return {
            'total_users': self.user_repo.count_users(),
            'admin_users': self.user_repo.count_admin_users(),
            'recent_users': len(self.user_repo.get_recent_users(5))
        }

    def create_amenity(self, amenity_data):
        """Create a new amenity and store in the repository."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information."""
        # Check name uniqueness if name is being updated
        if 'name' in amenity_data:
            if self.amenity_repo.name_exists(amenity_data['name'], exclude_id=amenity_id):
                raise ValueError("Amenity name already exists")
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def get_amenities_by_name_pattern(self, pattern):
        """Search amenities by name pattern."""
        return [amenity for amenity in self.amenity_repo.get_all() 
                if pattern.lower() in amenity.name.lower()]
    
    def get_recent_amenities(self, limit=10):
        """Get recently created amenities."""
        return self.amenity_repo.get_recent_amenities(limit)
    
    def get_amenity_statistics(self):
        """Get amenity statistics."""
        return {
            'total_amenities': self.amenity_repo.count_amenities(),
            'recent_amenities': len(self.amenity_repo.get_recent_amenities(5))
        }

    def create_place(self, place_data):
        """Create a new place and store in the repository."""
        # Validate owner exists
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        # Note: Amenity relationships will be handled when relationships are implemented
        # For now, we only validate that amenities exist but don't create the relationships
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
        
        # Create place with title
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude']
        )
        
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID, including associated owner and amenities."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        # Note: Owner and amenity relationships will be handled when relationships are implemented
        # For now, we only validate that referenced entities exist
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
        
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
        # Update fields directly
        for field in ['title', 'description', 'price', 'latitude', 'longitude']:
            if field in place_data:
                setattr(place, field, place_data[field])
        # Update the place in the repository
        return self.place_repo.update(place_id, place_data)
    
    def get_places_by_price_range(self, min_price, max_price):
        """Get places within a price range."""
        return self.place_repo.get_places_by_price_range(min_price, max_price)
    
    def get_places_by_location(self, latitude, longitude, radius_km=10):
        """Get places near a location."""
        return self.place_repo.get_places_by_location(latitude, longitude, radius_km)
    
    def search_places_by_title(self, pattern):
        """Search places by title pattern."""
        return self.place_repo.get_places_by_title_pattern(pattern)
    
    def get_recent_places(self, limit=10):
        """Get recently created places."""
        return self.place_repo.get_recent_places(limit)
    
    def get_places_ordered_by_price(self, ascending=True):
        """Get places ordered by price."""
        return self.place_repo.get_places_ordered_by_price(ascending)
    
    def get_place_statistics(self):
        """Get place statistics."""
        return self.place_repo.get_price_statistics()

    def create_review(self, review_data):
        """Create a new review and store in the repository."""
        # Validate user exists
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        # Validate exists
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        # Validate rating is between 1 and 5
        rating = review_data.get('rating')
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        # Create review (relationships will be handled later)
        review = Review(
            text=review_data.get('text', ''),
            rating=rating
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place."""
        # Validate place exists
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # Note: This functionality will be implemented when relationships are added
        # For now, return empty list since we don't have foreign key relationships yet
        return []

    def update_review(self, review_id, review_data):
        """Update a review's information."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Note: User and place relationships will be handled when relationships are implemented
        # For now, we only validate that referenced entities exist
        if 'user_id' in review_data:
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError("User not found")

        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")

        # Update fields directly
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        if 'text' in review_data:
            review.text = review_data['text']

        # Save updates the updated_at timestamp
        review.save()

        return review

    def delete_place(self, place_id):
        """Delete a place by ID."""
        return self.place_repo.delete(place_id)

    def delete_review(self, review_id):
        """Delete a review by ID."""
        return self.review_repo.delete(review_id)
    
    def get_reviews_by_rating(self, rating):
        """Get reviews with a specific rating."""
        return self.review_repo.get_reviews_by_rating(rating)
    
    def get_reviews_by_rating_range(self, min_rating, max_rating):
        """Get reviews within a rating range."""
        return self.review_repo.get_reviews_by_rating_range(min_rating, max_rating)
    
    def get_high_rated_reviews(self, min_rating=4):
        """Get reviews with high ratings."""
        return self.review_repo.get_high_rated_reviews(min_rating)
    
    def search_reviews_by_text(self, search_term):
        """Search reviews by text content."""
        return self.review_repo.search_reviews_by_text(search_term)
    
    def get_recent_reviews(self, limit=10):
        """Get recently created reviews."""
        return self.review_repo.get_recent_reviews(limit)
    
    def get_review_statistics(self):
        """Get comprehensive review statistics."""
        return self.review_repo.get_rating_statistics()
