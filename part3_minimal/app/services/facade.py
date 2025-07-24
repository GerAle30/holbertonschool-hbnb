from app import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    """Simplified facade for business logic"""
    
    # User operations
    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        user.save()
        return user
    
    def get_user(self, user_id):
        return User.query.get(user_id)
    
    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def get_all_users(self):
        return User.query.all()
    
    def update_user(self, user_id, user_data):
        user = User.query.get(user_id)
        if user:
            for key, value in user_data.items():
                if key == 'password':
                    user.hash_password(value)
                else:
                    setattr(user, key, value)
            user.save()
        return user
    
    # Place operations
    def create_place(self, place_data):
        place = Place(
            title=place_data['title'],
            description=place_data.get('description'),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )
        place.save()
        return place
    
    def get_place(self, place_id):
        return Place.query.get(place_id)
    
    def get_all_places(self):
        return Place.query.all()
    
    def update_place(self, place_id, place_data):
        place = Place.query.get(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)
            place.save()
        return place
    
    def delete_place(self, place_id):
        place = Place.query.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
            return True
        return False
    
    # Amenity operations
    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data['name'])
        amenity.save()
        return amenity
    
    def get_amenity(self, amenity_id):
        return Amenity.query.get(amenity_id)
    
    def get_all_amenities(self):
        return Amenity.query.all()
    
    def update_amenity(self, amenity_id, amenity_data):
        amenity = Amenity.query.get(amenity_id)
        if amenity:
            amenity.name = amenity_data['name']
            amenity.save()
        return amenity
    
    def delete_amenity(self, amenity_id):
        amenity = Amenity.query.get(amenity_id)
        if amenity:
            db.session.delete(amenity)
            db.session.commit()
            return True
        return False
    
    # Review operations
    def create_review(self, review_data):
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        review.save()
        return review
    
    def get_review(self, review_id):
        return Review.query.get(review_id)
    
    def get_all_reviews(self):
        return Review.query.all()
    
    def get_reviews_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()
    
    def update_review(self, review_id, review_data):
        review = Review.query.get(review_id)
        if review:
            for key, value in review_data.items():
                setattr(review, key, value)
            review.save()
        return review
    
    def delete_review(self, review_id):
        review = Review.query.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return True
        return False

# Global facade instance
facade = HBnBFacade()
