from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenities import Amenity
from app.models.place import Place
from app.models.reviews import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """Create new user and store in the repo."""
        # Extract password from user_data to handle separately
        user_data_copy = user_data.copy()
        password = user_data_copy.pop('password', None)
        
        # Create user without password
        user = User(**user_data_copy)
        
        # Hash password if provided
        if password:
            user.hash_password(password)
        
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a usr by id."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Find user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user's information."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
            
        # Handle password hashing if password is being updated
        if 'password' in user_data:
            password = user_data.pop('password')
            user.hash_password(password)
            
        # Update other fields directly on the user object
        for field, value in user_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
                
        # Update the user in the repository
        return self.user_repo.update(user_id, user_data)

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
        return self.amenity_repo.update(amenity_id, amenity_data)

    def create_place(self, place_data):
        """Create a new place and store in the repository."""
        # Validate owner exists
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        # Validate amenities exist
        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)
        # Create place with name instead of title to match model
        place = Place(
            name=place_data['title'],  # Map title
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        # Add amenities
        for amenity in amenities:
            place.add_amenity(amenity)
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
        # Validate owner  provided
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner
        # Validate amenities  provided
        if 'amenities' in place_data:
            amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                amenities.append(amenity)
            place.amenities = amenities
        # Update other fields
        if 'title' in place_data:
            place.name = place_data['title']  # Map title
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']
        # Update the place in the repository
        return self.place_repo.update(place_id, place_data)

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

        # Create (map 'text' to 'comment' to match model)
        review = Review(
            user=user,
            place=place,
            rating=rating,
            comment=review_data.get('text', '')
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

        # Use SQLAlchemy filtering capabilities
        # Note: This will need to be adjusted when models have proper relationships
        all_reviews = self.review_repo.get_all()
        place_reviews = []
        for review in all_reviews:
            if hasattr(review, 'place_id') and review.place_id == place_id:
                place_reviews.append(review)
            elif hasattr(review, 'place') and review.place.id == place_id:
                place_reviews.append(review)
        return place_reviews

    def update_review(self, review_id, review_data):
        """Update a review's information."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Validate user if provided
        if 'user_id' in review_data:
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError("User not found")
            review.user = user

        # Validate place if provided
        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            review.place = place

        # Validat rating if provided
        if 'rating' in review_data:
            rating = review_data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = rating

        # Update text\commnt if provided
        if 'text' in review_data:
            review.comment = review_data['text']

        # Save updates the updated_at timestamp
        review.save()

        return review

    def delete_place(self, place_id):
        """Delete a place by ID."""
        return self.place_repo.delete(place_id)

    def delete_review(self, review_id):
        """Delete a review by ID."""
        return self.review_repo.delete(review_id)
