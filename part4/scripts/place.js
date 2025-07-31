// API Configuration
const API_URL = 'http://localhost:5000/api'; // Adjust this to your API URL

// Cookie utility functions
function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

// Extract place ID from URL
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Check user authentication
function checkAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        // Store the token for later use
        return token;
    }
    return null;
}

// Fetch place details from API
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            
            // Also fetch reviews if authenticated
            if (token) {
                fetchReviews(token, placeId);
            }
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            // Load sample data for demo purposes
            loadSamplePlace(placeId);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        // Load sample data for demo purposes
        loadSamplePlace(placeId);
    }
}

// Fetch reviews for the place
async function fetchReviews(token, placeId) {
    try {
        const response = await fetch(`${API_URL}/places/${placeId}/reviews`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        } else {
            console.error('Failed to fetch reviews:', response.statusText);
            loadSampleReviews();
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        loadSampleReviews();
    }
}

// Display place details in the #place-details section
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    
    // Clear the current content of the place details section
    placeDetails.innerHTML = '';
    
    // Use sample images for demo
    const imageUrl = getRandomImage();
    
    // Create elements to display the place details
    placeDetails.innerHTML = `
        <div class="place-info">
            <h1>${place.name || place.title}</h1>
            <img src="${imageUrl}" alt="${place.name || place.title}" onerror="this.src='1.png'">
            
            <div class="info-grid">
                <div class="info-item">
                    <h3>Location</h3>
                    <p>${place.city || place.location || 'Unknown'}, ${place.country || 'Unknown'}</p>
                </div>
                <div class="info-item">
                    <h3>Host</h3>
                    <p>${place.host?.first_name || place.host_name || 'Host'} ${place.host?.last_name || ''}</p>
                </div>
                <div class="info-item">
                    <h3>Price per Night</h3>
                    <p class="price">$${place.price_per_night || place.price || 0}</p>
                </div>
                <div class="info-item">
                    <h3>Amenities</h3>
                    <div class="amenities-list">
                        ${formatAmenities(place.amenities || ['WiFi', 'Kitchen', 'Parking'])}
                    </div>
                </div>
            </div>
            
            <div class="info-item">
                <h3>Description</h3>
                <p>${place.description || 'A wonderful place to stay with all the amenities you need for a comfortable visit.'}</p>
            </div>
        </div>
        
        <div class="reviews-section">
            <h2>Reviews</h2>
            <div id="reviews-container">
                <!-- Reviews will be loaded here -->
            </div>
        </div>
    `;
}

// Display reviews
function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews-container');
    
    if (!reviews || reviews.length === 0) {
        reviewsContainer.innerHTML = '<p class="text-center">No reviews yet. Be the first to review this place!</p>';
        return;
    }
    
    reviewsContainer.innerHTML = '';
    
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        // Generate star rating
        const stars = '⭐'.repeat(review.rating || 5);
        
        reviewCard.innerHTML = `
            <div class="review-header">
                <span class="reviewer-name">${review.user?.first_name || review.user_name || 'Anonymous'} ${review.user?.last_name || ''}</span>
                <span class="rating">${stars} (${review.rating || 5}/5)</span>
            </div>
            <div class="review-comment">${review.comment || review.text || 'No comment provided.'}</div>
        `;
        
        reviewsContainer.appendChild(reviewCard);
    });
}

// Submit review
async function submitReview(event) {
    event.preventDefault();
    
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();
    
    if (!token) {
        showMessage('Please login to submit a review.', 'error');
        return;
    }
    
    const reviewText = document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;
    
    if (!reviewText.trim()) {
        showMessage('Please enter your review.', 'error');
        return;
    }
    
    if (!rating) {
        showMessage('Please select a rating.', 'error');
        return;
    }
    
    try {
        const submitButton = document.querySelector('.submit-button');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Submitting...';
        submitButton.disabled = true;
        
        const response = await fetch(`${API_URL}/places/${placeId}/reviews`, {
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
            showMessage('Review submitted successfully!', 'success');
            document.getElementById('review-form').reset();
            // Reload reviews
            fetchReviews(token, placeId);
        } else {
            const errorData = await response.json();
            showMessage(errorData.message || 'Failed to submit review.', 'error');
        }
        
    } catch (error) {
        console.error('Error submitting review:', error);
        showMessage('Failed to submit review. Please try again.', 'error');
    } finally {
        const submitButton = document.querySelector('.submit-button');
        submitButton.textContent = 'Submit Review';
        submitButton.disabled = false;
    }
}

// Show message
function showMessage(message, type) {
    const messageDiv = document.getElementById('review-message');
    messageDiv.textContent = message;
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    messageDiv.classList.remove('hidden');
    
    setTimeout(() => {
        messageDiv.classList.add('hidden');
    }, 5000);
}

// Format amenities with icons
function formatAmenities(amenities) {
    const amenityIcons = {
        'WiFi': 'icon_wifi.png',
        'Wifi': 'icon_wifi.png',
        'Internet': 'icon_wifi.png',
        'Kitchen': 'icon_bed.png', // Using bed icon as placeholder for kitchen
        'Bathroom': 'icon_bath.png',
        'Bath': 'icon_bath.png',
        'Bathtub': 'icon_bath.png',
        'Shower': 'icon_bath.png',
        'Bedroom': 'icon_bed.png',
        'Bed': 'icon_bed.png',
        'Sleeping': 'icon_bed.png'
    };
    
    return amenities.map(amenity => {
        const icon = amenityIcons[amenity];
        if (icon) {
            return `<div class="amenity-item"><img src="${icon}" alt="${amenity}" class="amenity-icon"> ${amenity}</div>`;
        } else {
            return `<div class="amenity-item">• ${amenity}</div>`;
        }
    }).join('');
}

// Get random image for demo purposes
function getRandomImage() {
    const images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png'];
    return images[Math.floor(Math.random() * images.length)];
}

// Load sample place for demo purposes
function loadSamplePlace(placeId) {
    const samplePlaces = {
        '1': {
            name: 'Cozy Apartment in Paris',
            city: 'Paris',
            country: 'France',
            price_per_night: 120,
            host: { first_name: 'Marie', last_name: 'Dubois' },
            description: 'A charming apartment in the heart of Paris, perfect for exploring the city. Walking distance to major attractions.',
            amenities: ['WiFi', 'Kitchen', 'Bathroom', 'Bedroom']
        },
        '2': {
            name: 'Modern Loft in New York',
            city: 'New York',
            country: 'United States',
            price_per_night: 200,
            host: { first_name: 'John', last_name: 'Smith' },
            description: 'A stylish loft in Manhattan with stunning city views. Perfect for business or leisure travelers.',
            amenities: ['WiFi', 'Bed', 'Bath', 'Internet']
        },
        '3': {
            name: 'Beach House in Barcelona',
            city: 'Barcelona',
            country: 'Spain',
            price_per_night: 150,
            host: { first_name: 'Carlos', last_name: 'Rodriguez' },
            description: 'Beautiful house near the beach with amazing sea views.',
            amenities: ['Wifi', 'Bedroom', 'Shower', 'Beach Access']
        }
    };
    
    const place = samplePlaces[placeId] || samplePlaces['1'];
    displayPlaceDetails(place);
    loadSampleReviews();
}

// Load sample reviews for demo purposes
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

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', () => {
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }
    
    // Check user authentication
    const token = checkAuthentication();
    
    // Fetch place details
    if (token) {
        fetchPlaceDetails(token, placeId);
    } else {
        // Load sample data for non-authenticated users
        loadSamplePlace(placeId);
    }
    
    // Add review form submission handler
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', submitReview);
    }
});
