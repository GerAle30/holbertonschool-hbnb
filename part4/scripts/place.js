// Include auth utilities
document.head.appendChild(Object.assign(document.createElement('script'), {src: 'scripts/auth.js'}));

document.addEventListener('DOMContentLoaded', function() {
    const placeInfo = document.getElementById('place-info');
    const reviewsContainer = document.getElementById('reviews-container');
    const addReviewSection = document.getElementById('add-review-section');
    const reviewForm = document.getElementById('review-form');
    const reviewMessage = document.getElementById('review-message');

    // Get place ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    // Show add review section only for authenticated users
    if (isAuthenticated()) {
        addReviewSection.classList.remove('hidden');
    }

    // Load place details and reviews
    loadPlaceDetails();
    loadReviews();

    // Add review form submission
    reviewForm.addEventListener('submit', submitReview);

    async function loadPlaceDetails() {
        try {
            const token = getToken();
            const response = await fetch(`${AUTH_API_URL}/places/${placeId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch place details');
            }

            const place = await response.json();
            displayPlaceDetails(place);

        } catch (error) {
            console.error('Error loading place details:', error);
            // Load sample place for demo
            loadSamplePlace();
        }
    }

    function displayPlaceDetails(place) {
        const imageUrl = getRandomImage();
        
        placeInfo.innerHTML = `
            <h1>${place.name || place.title}</h1>
            <img src="${imageUrl}" alt="${place.name || place.title}" onerror="this.src='1.png'">
            
            <div class="info-grid">
                <div class="info-item">
                    <h3>Location</h3>
                    <p>${place.city || place.location}, ${place.country}</p>
                </div>
                <div class="info-item">
                    <h3>Host</h3>
                    <p>${place.host?.first_name || place.host_name || 'Host'} ${place.host?.last_name || ''}</p>
                </div>
                <div class="info-item">
                    <h3>Price per Night</h3>
                    <p class="price">$${place.price_per_night || place.price}</p>
                </div>
                <div class="info-item">
                    <h3>Amenities</h3>
                    <p>${place.amenities ? place.amenities.join(', ') : 'WiFi, Kitchen, Parking'}</p>
                </div>
            </div>
            
            <div class="info-item">
                <h3>Description</h3>
                <p>${place.description || 'A wonderful place to stay with all the amenities you need for a comfortable visit.'}</p>
            </div>
        `;
    }

    async function loadReviews() {
        try {
            const token = getToken();
            const response = await fetch(`${AUTH_API_URL}/places/${placeId}/reviews`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch reviews');
            }

            const reviews = await response.json();
            displayReviews(reviews);

        } catch (error) {
            console.error('Error loading reviews:', error);
            // Load sample reviews for demo
            loadSampleReviews();
        }
    }

    function displayReviews(reviews) {
        if (reviews.length === 0) {
            reviewsContainer.innerHTML = '<p class="text-center">No reviews yet. Be the first to review this place!</p>';
            return;
        }

        reviews.forEach(review => {
            const reviewCard = createReviewCard(review);
            reviewsContainer.appendChild(reviewCard);
        });
    }

    function createReviewCard(review) {
        const card = document.createElement('div');
        card.className = 'review-card';
        
        // Generate star rating
        const stars = '⭐'.repeat(review.rating || 5);
        
        card.innerHTML = `
            <div class="review-header">
                <span class="reviewer-name">${review.user?.first_name || review.user_name || 'Anonymous'} ${review.user?.last_name || ''}</span>
                <span class="rating">${stars} (${review.rating || 5}/5)</span>
            </div>
            <div class="review-comment">${review.comment || review.text}</div>
        `;
        
        return card;
    }

    async function submitReview(e) {
        e.preventDefault();

        if (!isAuthenticated()) {
            showReviewMessage('Please login to submit a review.', 'error');
            return;
        }

        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;

        try {
            const submitButton = reviewForm.querySelector('.submit-button');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Submitting...';
            submitButton.disabled = true;

            const token = getToken();
            const response = await fetch(`${AUTH_API_URL}/places/${placeId}/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    comment: reviewText,
                    rating: parseInt(rating)
                })
            });

            if (response.ok) {
                showReviewMessage('Review submitted successfully!', 'success');
                reviewForm.reset();
                // Reload reviews
                reviewsContainer.innerHTML = '';
                loadReviews();
            } else {
                const errorData = await response.json();
                showReviewMessage(errorData.message || 'Failed to submit review.', 'error');
            }

        } catch (error) {
            console.error('Error submitting review:', error);
            showReviewMessage('Failed to submit review. Please try again.', 'error');
        } finally {
            const submitButton = reviewForm.querySelector('.submit-button');
            submitButton.textContent = 'Submit Review';
            submitButton.disabled = false;
        }
    }

    function showReviewMessage(message, type) {
        reviewMessage.textContent = message;
        reviewMessage.className = type === 'success' ? 'success-message' : 'error-message';
        reviewMessage.classList.remove('hidden');
        
        setTimeout(() => {
            reviewMessage.classList.add('hidden');
        }, 5000);
    }

    function getRandomImage() {
        const images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png'];
        return images[Math.floor(Math.random() * images.length)];
    }

    // Sample data for demo purposes
    function loadSamplePlace() {
        const samplePlaces = {
            '1': {
                name: 'Cozy Apartment in Paris',
                city: 'Paris',
                country: 'France',
                price_per_night: 120,
                host: { first_name: 'Marie', last_name: 'Dubois' },
                description: 'A charming apartment in the heart of Paris, perfect for exploring the city. Walking distance to major attractions.',
                amenities: ['WiFi', 'Kitchen', 'Air Conditioning', 'Parking']
            },
            '2': {
                name: 'Modern Loft in New York',
                city: 'New York',
                country: 'United States',
                price_per_night: 200,
                host: { first_name: 'John', last_name: 'Smith' },
                description: 'A stylish loft in Manhattan with stunning city views. Perfect for business or leisure travelers.',
                amenities: ['WiFi', 'Gym Access', 'Concierge', 'Pet Friendly']
            }
        };

        const place = samplePlaces[placeId] || samplePlaces['1'];
        displayPlaceDetails(place);
    }

    function loadSampleReviews() {
        const sampleReviews = [
            {
                user: { first_name: 'Alice', last_name: 'Johnson' },
                rating: 5,
                comment: 'Amazing place! The host was very welcoming and the location is perfect. Highly recommended!'
            },
            {
                user: { first_name: 'Bob', last_name: 'Wilson' },
                rating: 4,
                comment: 'Great stay overall. The place was clean and comfortable. Would definitely come back.'
            },
            {
                user: { first_name: 'Carol', last_name: 'Davis' },
                rating: 5,
                comment: 'Exceeded all expectations! Beautiful place, excellent amenities, and wonderful host.'
            }
        ];

        displayReviews(sampleReviews);
    }
});
