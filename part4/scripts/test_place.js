// Mock API and place details logic for testing
// Include auth utilities
document.head.appendChild(Object.assign(document.createElement('script'), {src: 'scripts/auth.js'}));

// API Configuration
const API_URL = 'http://localhost:5000/api';

// Cookie utility functions
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

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

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// Get place ID from URL
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
        return token;
    }
    return null;
}

// Check authentication and update status
function updateAuthStatus() {
    const authStatus = document.getElementById('auth-status');
    const token = getCookie('token');

    if (token) {
        authStatus.textContent = `Authenticated with token: ${token.substring(0, 10)}...`;
    } else {
        authStatus.textContent = 'Not authenticated';
    }
}

// Fetch place details (mock)
function fetchPlaceDetailsMock(placeId) {
    const samplePlaces = {
        '1': {
            name: 'Cozy Apartment in Paris',
            city: 'Paris',
            country: 'France',
            price_per_night: 120,
            host: { first_name: 'Marie', last_name: 'Dubois' },
            description: 'A charming apartment in the heart of Paris, perfect for exploring the city. Walking distance to major attractions.',
            amenities: ['WiFi', 'Kitchen', 'Air Conditioning', 'Parking'],
            reviews: [
                { user: { first_name: 'Alice', last_name: 'Johnson' }, rating: 5, comment: 'Amazing place! Highly recommended!' },
                { user: { first_name: 'Bob', last_name: 'Smith' }, rating: 4, comment: 'Great location and host!' }
            ]
        },
        '2': {
            name: 'Modern Loft in New York',
            city: 'New York',
            country: 'United States',
            price_per_night: 200,
            host: { first_name: 'John', last_name: 'Smith' },
            description: 'A stylish loft in Manhattan with stunning city views.',
            amenities: ['WiFi', 'Gym Access', 'Concierge', 'Pet Friendly'],
            reviews: [
                { user: { first_name: 'Jane', last_name: 'Doe' }, rating: 5, comment: 'Luxurious experience!' },
                { user: { first_name: 'Charlie', last_name: 'Brown' }, rating: 4, comment: 'Fantastic amenities and service.' }
            ]
        }
    };
    return samplePlaces[placeId];
}

// Display place details
function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');

    if (!place) {
        placeDetails.innerHTML = '<p>Place details not found.</p>';
        return;
    }

    const imageUrl = getRandomImage();

    placeDetails.innerHTML = `
        <div class="place-info">
            <h1>${place.name}</h1>
            <img src="${imageUrl}" alt="${place.name}" onerror="this.src='1.png'">
            
            <div class="info-grid">
                <div class="info-item">
                    <h3>Location</h3>
                    <p>${place.city}, ${place.country}</p>
                </div>
                <div class="info-item">
                    <h3>Host</h3>
                    <p>${place.host.first_name} ${place.host.last_name}</p>
                </div>
                <div class="info-item">
                    <h3>Price per Night</h3>
                    <p class="price">$${place.price_per_night}/night</p>
                </div>
                <div class="info-item">
                    <h3>Amenities</h3>
                    <p>${place.amenities.join(', ')}</p>
                </div>
            </div>
            
            <div class="info-item">
                <h3>Description</h3>
                <p>${place.description}</p>
            </div>
        </div>
        
        <div class="reviews-section">
            <h2>Reviews</h2>
            <div id="reviews-container">
                <!-- Reviews will be loaded here -->
            </div>
        </div>
    `;
    displayReviews(place.reviews);
}

// Display reviews
function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews-container');

    if (!reviews || !reviews.length) {
        reviewsContainer.innerHTML = '<p>No reviews yet. Be the first to review this place!</p>';
        return;
    }

    reviewsContainer.innerHTML = '';
    reviews.forEach(review => {
        const stars = '⭐'.repeat(review.rating);
        reviewsContainer.innerHTML += `
            <div class="review-card">
                <div class="review-header">
                    <span class="reviewer-name">${review.user.first_name} ${review.user.last_name}</span>
                    <span class="rating">${stars} (${review.rating}/5)</span>
                </div>
                <div class="review-comment">${review.comment}</div>
            </div>
        `;
    });
}

// Simulate review submission
function simulateReviewSubmission() {
    const placeId = getPlaceIdFromURL();
    const place = fetchPlaceDetailsMock(placeId);

    const newReview = {
        user: { first_name: 'Simulated', last_name: 'User' },
        rating: parseInt(document.getElementById('rating').value),
        comment: document.getElementById('review-text').value
    };

    place.reviews.push(newReview);
    document.getElementById('review-form').reset();
    displayReviews(place.reviews);
    showMessage('Review submitted successfully!', 'success');
}

// Submit review
function submitReview(event) {
    event.preventDefault();
    const token = getCookie('token');

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

    simulateReviewSubmission(); // Simulate without backend
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

// Get random image
function getRandomImage() {
    const images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png'];
    return images[Math.floor(Math.random() * images.length)];
}

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', function() {
    const authStatus = document.getElementById('auth-status');
    const simulateLoginButton = document.getElementById('simulate-login');
    const clearAuthButton = document.getElementById('clear-auth');
    const reviewForm = document.getElementById('review-form');

    const placeId = getPlaceIdFromURL();
    const place = fetchPlaceDetailsMock(placeId);
    displayPlaceDetails(place);
    updateAuthStatus();

    simulateLoginButton.addEventListener('click', () => {
        setCookie('token', 'mock_jwt_token');
        updateAuthStatus();
        checkAuthentication();
    });

    clearAuthButton.addEventListener('click', () => {
        deleteCookie('token');
        updateAuthStatus();
        checkAuthentication();
    });

    reviewForm.addEventListener('submit', submitReview);
});

