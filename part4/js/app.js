// HBNB Frontend Application JavaScript

// Authentication state management
let isLoggedIn = false;

// Check login state on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in (in real app, this would check tokens/session)
    isLoggedIn = localStorage.getItem('hbnb_logged_in') === 'true';
    
    updateAuthState();
    loadPlaces();
});

// Update UI based on authentication state
function updateAuthState() {
    if (isLoggedIn) {
        document.body.classList.add('logged-in');
        
        // Update login button to logout
        const loginButtons = document.querySelectorAll('.login-button');
        loginButtons.forEach(button => {
            if (button.textContent === 'Login') {
                button.textContent = 'Logout';
                button.href = '#';
                button.addEventListener('click', logout);
            }
        });
    } else {
        document.body.classList.remove('logged-in');
    }
}

// Login function
function login(email, password) {
    // Simulate login process - in real app this would validate credentials
    if (email && password) {
        isLoggedIn = true;
        localStorage.setItem('hbnb_logged_in', 'true');
        localStorage.setItem('hbnb_user_email', email);
        updateAuthState();
        return true;
    }
    return false;
}

// Logout function
function logout(e) {
    if (e) e.preventDefault();
    
    isLoggedIn = false;
    localStorage.removeItem('hbnb_logged_in');
    localStorage.removeItem('hbnb_user_email');
    updateAuthState();
    
    // Redirect to home page
    window.location.href = 'index.html';
}

// Sample places data
const samplePlaces = [
    {
        id: 1,
        name: "Cozy Downtown Apartment",
        price: 100,
        image: "images/sample1.jpg",
        host: "John Doe",
        description: "A beautiful and cozy apartment located in the heart of downtown.",
        amenities: ["WiFi", "Air Conditioning", "Kitchen", "Parking", "TV", "Washing Machine"],
        reviews: [
            {
                author: "Alice Smith",
                rating: 5,
                comment: "Amazing place! The location is perfect and the host was very accommodating."
            },
            {
                author: "Bob Johnson", 
                rating: 4,
                comment: "Great apartment with all the necessary amenities. Very clean and comfortable."
            }
        ]
    },
    {
        id: 2,
        name: "Modern Loft Space",
        price: 150,
        image: "images/sample2.jpg",
        host: "Jane Smith",
        description: "A stylish modern loft with great city views and contemporary amenities.",
        amenities: ["WiFi", "Air Conditioning", "Kitchen", "Gym Access", "TV", "Balcony"],
        reviews: [
            {
                author: "Carol Wilson",
                rating: 5,
                comment: "Excellent stay! The apartment exceeded my expectations."
            }
        ]
    }
];

// Load and display places
function loadPlaces() {
    const placesGrid = document.querySelector('.places-grid');
    if (!placesGrid) return;

    placesGrid.innerHTML = '';
    
    samplePlaces.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <img src="${place.image}" alt="${place.name}">
            <h3>${place.name}</h3>
            <p class="place-price">$${place.price}/night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesGrid.appendChild(placeCard);
    });
}

// Get place details by ID from URL parameters
function getPlaceFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = parseInt(urlParams.get('id')) || 1;
    return samplePlaces.find(place => place.id === placeId) || samplePlaces[0];
}

// Load place details on place.html page
function loadPlaceDetails() {
    if (!window.location.pathname.includes('place.html')) return;
    
    const place = getPlaceFromUrl();
    
    // Update page title and content
    document.title = `HBNB - ${place.name}`;
    document.querySelector('h1').textContent = place.name;
    
    // Update place details (this would normally be done server-side)
    const placeInfo = document.querySelector('.place-info');
    if (placeInfo) {
        placeInfo.innerHTML = `
            <div>
                <h4>Host Information</h4>
                <p><strong>Host:</strong> ${place.host}</p>
                <p><strong>Email:</strong> ${place.host.toLowerCase().replace(' ', '.')}@example.com</p>
            </div>
            
            <div>
                <h4>Price & Details</h4>
                <p><strong>Price per night:</strong> $${place.price}</p>
                <p><strong>Location:</strong> Downtown Area</p>
            </div>
            
            <div style="grid-column: 1 / -1;">
                <h4>Description</h4>
                <p>${place.description}</p>
            </div>
            
            <div style="grid-column: 1 / -1;">
                <h4>Amenities</h4>
                <ul class="amenities-list">
                    ${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    // Load reviews
    loadReviews(place.reviews);
}

// Load reviews for a place
function loadReviews(reviews) {
    const reviewsSection = document.querySelector('.reviews-section');
    if (!reviewsSection) return;
    
    const reviewsContainer = reviewsSection.querySelector('.review-card')?.parentNode || reviewsSection;
    
    // Clear existing review cards
    const existingReviews = reviewsContainer.querySelectorAll('.review-card');
    existingReviews.forEach(review => review.remove());
    
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <div class="review-header">
                <span class="review-author">${review.author}</span>
                <span class="review-rating">${'⭐'.repeat(review.rating)} ${review.rating}/5</span>
            </div>
            <p class="review-comment">${review.comment}</p>
        `;
        reviewsContainer.appendChild(reviewCard);
    });
}

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            field.style.borderColor = '#ddd';
        }
    });
    
    return isValid;
}

// Initialize place details when page loads
document.addEventListener('DOMContentLoaded', loadPlaceDetails);
