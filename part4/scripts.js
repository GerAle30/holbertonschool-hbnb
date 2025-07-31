// HBNB Frontend Scripts with API Integration

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api/v1'; // Update this with your actual API URL

// Cookie utility functions
function setCookie(name, value, days = 7) {
    const expires = new Date();
    expires.setTime(expires.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = `${name}=${value}; expires=${expires.toUTCString()}; path=/`;
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

// Check if user is logged in
function isLoggedIn() {
    return getCookie('token') !== null;
}

// Get current user token
function getAuthToken() {
    return getCookie('token');
}

// Get place ID from URL query parameters
function getPlaceIdFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('id');
}

// Check user authentication and control UI (for index page)
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    
    if (!token) {
        if (loginLink) {
            loginLink.style.display = 'block';
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
        }
        // Show sample places for non-authenticated users
        displaySamplePlaces();
    } else {
        if (loginLink) {
            loginLink.style.display = 'block';
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        }
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}

// Check user authentication for place details page
function checkAuthenticationForPlace() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const loginLink = document.getElementById('login-link');
    
    // Update login/logout button
    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
            loginLink.textContent = 'Login';
            loginLink.href = 'login.html';
        } else {
            loginLink.style.display = 'block';
            loginLink.textContent = 'Logout';
            loginLink.href = '#';
            loginLink.addEventListener('click', (e) => {
                e.preventDefault();
                logout();
            });
        }
    }
    
    // Show/hide add review form based on authentication
    if (addReviewSection) {
        if (!token) {
            addReviewSection.style.display = 'none';
        } else {
            addReviewSection.style.display = 'block';
        }
    }
    
    // Get place ID and fetch details
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        if (token) {
            fetchPlaceDetails(token, placeId);
        } else {
            // Show sample place details for non-authenticated users
            displaySamplePlaceDetails(placeId);
        }
    } else {
        showError('No place ID provided in URL');
    }
}

// Login function with API integration
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            // Store JWT token in cookie
            setCookie('token', data.access_token);
            return { success: true, data };
        } else {
            const errorData = await response.json();
            return { success: false, error: errorData.message || 'Login failed' };
        }
    } catch (error) {
        console.error('Login error:', error);
        return { success: false, error: 'Network error. Please try again.' };
    }
}

// Logout function
function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

// Update UI based on authentication state
function updateAuthUI() {
    const loginButtons = document.querySelectorAll('.login-button');
    const authOnlyElements = document.querySelectorAll('.auth-only');
    const guestOnlyElements = document.querySelectorAll('.guest-only');

    if (isLoggedIn()) {
        document.body.classList.add('logged-in');
        
        // Update login buttons to logout
        loginButtons.forEach(button => {
            if (button.textContent.trim() === 'Login') {
                button.textContent = 'Logout';
                button.href = '#';
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    logout();
                });
            }
        });

        // Show authenticated content
        authOnlyElements.forEach(el => el.style.display = 'block');
        guestOnlyElements.forEach(el => el.style.display = 'none');
    } else {
        document.body.classList.remove('logged-in');
        
        // Hide authenticated content
        authOnlyElements.forEach(el => el.style.display = 'none');
        guestOnlyElements.forEach(el => el.style.display = 'block');
    }
}

// Make authenticated API requests
async function makeAuthenticatedRequest(url, options = {}) {
    const token = getAuthToken();
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };

    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };

    try {
        const response = await fetch(url, mergedOptions);
        
        // Handle token expiration
        if (response.status === 401) {
            deleteCookie('token');
            window.location.href = 'login.html';
            return null;
        }
        
        return response;
    } catch (error) {
        console.error('API request error:', error);
        throw error;
    }
}

// Fetch places data from API with authentication
async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
            return places;
        } else {
            console.error('Failed to fetch places:', response.statusText);
            // Fallback to sample data if API fails
            displaySamplePlaces();
            return null;
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        displaySamplePlaces();
        return null;
    }
}

// Load places from API (wrapper function)
async function loadPlaces() {
    const token = getAuthToken();
    if (token) {
        await fetchPlaces(token);
    } else {
        displaySamplePlaces();
    }
}

// Display places in the grid
function displayPlaces(places) {
    const placesGrid = document.querySelector('.places-grid');
    if (!placesGrid) return;

    placesGrid.innerHTML = '';
    
    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <img src="${place.image || 'images/sample1.jpg'}" alt="${place.name}">
            <h3>${place.name}</h3>
            <p class="place-price">$${place.price}/night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        placesGrid.appendChild(placeCard);
    });
}

// Fallback sample places display
function displaySamplePlaces() {
    const placesGrid = document.querySelector('.places-grid');
    if (!placesGrid) return;

    const samplePlaces = [
        { id: 1, name: "Budget Hostel Room", price: 25, image: "images/sample1.jpg" },
        { id: 2, name: "Shared Apartment", price: 45, image: "images/sample2.jpg" },
        { id: 3, name: "Cozy Downtown Apartment", price: 85, image: "images/sample1.jpg" },
        { id: 4, name: "Modern Loft Space", price: 120, image: "images/sample2.jpg" },
        { id: 5, name: "Luxury Penthouse", price: 250, image: "images/sample1.jpg" },
        { id: 6, name: "Beach House Villa", price: 180, image: "images/sample2.jpg" }
    ];

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

// Fetch place details from API with authentication
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
            await loadPlaceReviews(placeId);
            return place;
        } else {
            console.error('Failed to fetch place details:', response.statusText);
            // Fallback to sample data if API fails
            displaySamplePlaceDetails(placeId);
            return null;
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
        displaySamplePlaceDetails(placeId);
        return null;
    }
}

// Load place details from API (wrapper function)
async function loadPlaceDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    
    if (!placeId) {
        showError('No place ID provided in URL');
        return;
    }

    const token = getAuthToken();
    if (token) {
        await fetchPlaceDetails(token, placeId);
    } else {
        displaySamplePlaceDetails(placeId);
    }
}

// Display place details (clear and populate the #place-details section)
function displayPlaceDetails(place) {
    // Update page title and main heading
    document.title = `HBNB - ${place.name}`;
    const placeTitle = document.getElementById('place-title');
    if (placeTitle) {
        placeTitle.textContent = place.name;
    }

    // Clear the current content of the place details section
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) return;
    
    placeDetailsSection.innerHTML = '';
    
    // Create place image
    const placeImage = document.createElement('img');
    placeImage.src = place.image || 'images/sample1.jpg';
    placeImage.alt = place.name;
    placeImage.style.cssText = 'width: 100%; height: 300px; object-fit: cover; border-radius: 10px; margin-bottom: 2rem;';
    placeDetailsSection.appendChild(placeImage);
    
    // Create place info grid
    const placeInfoGrid = document.createElement('div');
    placeInfoGrid.className = 'place-info';
    placeInfoGrid.innerHTML = `
        <div>
            <h4>Host Information</h4>
            <p><strong>Host:</strong> ${place.host_name || place.host || 'N/A'}</p>
            <p><strong>Email:</strong> ${place.host_email || 'N/A'}</p>
        </div>
        
        <div>
            <h4>Price & Details</h4>
            <p><strong>Price per night:</strong> $${place.price}</p>
            <p><strong>Location:</strong> ${place.location || 'Downtown Area'}</p>
        </div>
        
        <div style="grid-column: 1 / -1;">
            <h4>Description</h4>
            <p>${place.description || 'No description available.'}</p>
        </div>
        
        <div style="grid-column: 1 / -1;">
            <h4>Amenities</h4>
            <ul class="amenities-list">
                ${place.amenities ? place.amenities.map(amenity => `<li>${amenity}</li>`).join('') : '<li>No amenities listed</li>'}
            </ul>
        </div>
    `;
    placeDetailsSection.appendChild(placeInfoGrid);
}

// Display sample place details for non-authenticated users
function displaySamplePlaceDetails(placeId) {
    const samplePlaces = {
        '1': {
            id: 1,
            name: "Budget Hostel Room",
            price: 25,
            image: "images/sample1.jpg",
            host: "Sarah Johnson",
            location: "City Center",
            description: "A comfortable and affordable hostel room perfect for budget travelers. Clean facilities and friendly staff.",
            amenities: ["WiFi", "Shared Kitchen", "Lockers", "24/7 Reception"]
        },
        '2': {
            id: 2,
            name: "Shared Apartment",
            price: 45,
            image: "images/sample2.jpg",
            host: "Mike Chen",
            location: "Suburban Area",
            description: "A nice shared apartment with common areas and a great community atmosphere.",
            amenities: ["WiFi", "Kitchen", "Living Room", "Washing Machine"]
        },
        '3': {
            id: 3,
            name: "Cozy Downtown Apartment",
            price: 85,
            image: "images/sample1.jpg",
            host: "John Doe",
            location: "Downtown Area",
            description: "A beautiful and cozy apartment located in the heart of downtown. Perfect for business travelers and tourists alike.",
            amenities: ["WiFi", "Air Conditioning", "Kitchen", "Parking", "TV", "Washing Machine"]
        },
        '4': {
            id: 4,
            name: "Modern Loft Space",
            price: 120,
            image: "images/sample2.jpg",
            host: "Jane Smith",
            location: "Arts District",
            description: "A stylish modern loft with great city views and contemporary amenities.",
            amenities: ["WiFi", "Air Conditioning", "Kitchen", "Gym Access", "TV", "Balcony"]
        },
        '5': {
            id: 5,
            name: "Luxury Penthouse",
            price: 250,
            image: "images/sample1.jpg",
            host: "Robert Wilson",
            location: "Uptown",
            description: "An exclusive luxury penthouse with premium amenities and stunning views.",
            amenities: ["WiFi", "Air Conditioning", "Full Kitchen", "Private Pool", "Concierge", "Valet Parking"]
        },
        '6': {
            id: 6,
            name: "Beach House Villa",
            price: 180,
            image: "images/sample2.jpg",
            host: "Maria Garcia",
            location: "Beachfront",
            description: "A beautiful beach house villa with direct beach access and ocean views.",
            amenities: ["WiFi", "Kitchen", "Beach Access", "BBQ Grill", "Outdoor Shower", "Parking"]
        }
    };
    
    const place = samplePlaces[placeId] || samplePlaces['1'];
    displayPlaceDetails(place);
    
    // Display sample reviews
    const sampleReviews = [
        {
            user_name: "Alice Smith",
            rating: 5,
            comment: "Amazing place! The location is perfect and the host was very accommodating. Would definitely stay here again."
        },
        {
            user_name: "Bob Johnson",
            rating: 4,
            comment: "Great place with all the necessary amenities. Very clean and comfortable. Only minor issue was the noise from the street at night."
        },
        {
            user_name: "Carol Wilson",
            rating: 5,
            comment: "Excellent stay! The place exceeded my expectations. Perfect for a weekend getaway."
        }
    ];
    
    displayReviews(sampleReviews);
}

// Load reviews for a place
async function loadPlaceReviews(placeId) {
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/places/${placeId}/reviews`);
        
        if (response && response.ok) {
            const reviews = await response.json();
            displayReviews(reviews);
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

// Display reviews
function displayReviews(reviews) {
    const reviewsSection = document.querySelector('.reviews-section');
    if (!reviewsSection) return;

    // Clear existing reviews
    const existingReviews = reviewsSection.querySelectorAll('.review-card');
    existingReviews.forEach(review => review.remove());

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <div class="review-header">
                <span class="review-author">${review.user_name || 'Anonymous'}</span>
                <span class="review-rating">${'⭐'.repeat(review.rating)} ${review.rating}/5</span>
            </div>
            <p class="review-comment">${review.comment}</p>
        `;
        reviewsSection.appendChild(reviewCard);
    });
}

// Submit review
async function submitReview(placeId, rating, comment) {
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            body: JSON.stringify({
                rating: parseInt(rating),
                comment: comment
            })
        });

        if (response && response.ok) {
            return { success: true };
        } else {
            const errorData = await response.json();
            return { success: false, error: errorData.message || 'Failed to submit review' };
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        return { success: false, error: 'Network error. Please try again.' };
    }
}

// Form validation
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
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

// Show error message
function showError(message, containerId = null) {
    const container = containerId ? document.getElementById(containerId) : document.body;
    
    // Remove existing error messages
    const existingErrors = container.querySelectorAll('.error-message');
    existingErrors.forEach(error => error.remove());

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        margin: 10px 0;
    `;
    errorDiv.textContent = message;

    if (containerId) {
        container.insertBefore(errorDiv, container.firstChild);
    } else {
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(errorDiv, main.firstChild);
        }
    }

    // Auto-remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Show success message
function showSuccess(message, containerId = null) {
    const container = containerId ? document.getElementById(containerId) : document.body;
    
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.style.cssText = `
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        margin: 10px 0;
    `;
    successDiv.textContent = message;

    if (containerId) {
        container.insertBefore(successDiv, container.firstChild);
    } else {
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(successDiv, main.firstChild);
        }
    }

    // Auto-remove after 3 seconds
    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    
    // Handle login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            if (!validateForm(loginForm)) {
                showError('Please fill in all required fields.');
                return;
            }

            // Show loading state
            const submitButton = loginForm.querySelector('.submit-button');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Logging in...';
            submitButton.disabled = true;

            const result = await loginUser(email, password);
            
            // Reset button state
            submitButton.textContent = originalText;
            submitButton.disabled = false;

            if (result.success) {
                showSuccess('Login successful! Redirecting...');
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1000);
            } else {
                showError(result.error);
            }
        });
    }

    // Handle add review form
    const addReviewForm = document.getElementById('add-review-form');
    if (addReviewForm) {
        addReviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const urlParams = new URLSearchParams(window.location.search);
            const placeId = urlParams.get('place_id') || '1'; // Default for demo
            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value;
            
            if (!validateForm(addReviewForm)) {
                showError('Please fill in all required fields.');
                return;
            }

            const result = await submitReview(placeId, rating, comment);
            
            if (result.success) {
                showSuccess('Review submitted successfully!');
                setTimeout(() => {
                    window.location.href = `place.html?id=${placeId}`;
                }, 1000);
            } else {
                showError(result.error);
            }
        });
    }

    // Handle price filter on index page
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');
            
            placeCards.forEach(card => {
                const priceText = card.querySelector('.place-price').textContent;
                // Extract numeric price from text like "$100/night"
                const price = parseInt(priceText.replace(/[^0-9]/g, ''));
                
                if (selectedPrice === 'all') {
                    card.style.display = 'block';
                } else {
                    const maxPrice = parseInt(selectedPrice);
                    if (price <= maxPrice) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    }
    
    // Handle review form on place details page
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const placeId = getPlaceIdFromURL();
            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value;
            
            if (!validateForm(reviewForm)) {
                showError('Please fill in all required fields.');
                return;
            }

            const result = await submitReview(placeId, rating, comment);
            
            if (result.success) {
                showSuccess('Review submitted successfully!');
                // Reload the page to show the new review
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                showError(result.error);
            }
        });
    }
    
    // Check authentication and load content based on page
    if (window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/')) {
        checkAuthentication();
    } else if (window.location.pathname.includes('place.html')) {
        checkAuthenticationForPlace();
    }
});
