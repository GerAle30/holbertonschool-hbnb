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

// Check user authentication and redirect if not authenticated (for add review page)
function checkAuthenticationForAddReview() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return null;
    }
    return token;
}

// Check user authentication for place details page
function checkAuthenticationForPlace() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');
    const loginLink = document.getElementById('login-link');
    
    // Get place ID first
    const placeId = getPlaceIdFromURL();
    
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
            
            // Setup add review link
            const addReviewLink = document.getElementById('add-review-link');
            if (addReviewLink && placeId) {
                addReviewLink.href = `add_review.html?place_id=${placeId}`;
            }
        }
    }
    
    // Fetch place details
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

// Check user authentication for index page
function checkAuthenticationForIndex() {
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

// Login function with API integration and demo fallback
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
        
        // Demo fallback login (for testing purposes)
        if (email && password) {
            console.log('Using demo login fallback');
            // Generate a demo token
            const demoToken = 'demo_token_' + Date.now();
            setCookie('token', demoToken);
            return { success: true, data: { access_token: demoToken, user: { email } } };
        }
        
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
        { id: 1, name: "Budget Hostel Room", price: 25, image: "images/Budget Hostel Room.png" },
        { id: 2, name: "Shared Apartment", price: 45, image: "images/Shared Apartment.png" },
        { id: 3, name: "Cozy Downtown Apartment", price: 85, image: "images/Cozy Downtown Apartment.png" },
        { id: 4, name: "Modern Loft Space", price: 120, image: "images/Modern Loft Space.png" },
        { id: 5, name: "Luxury Penthouse", price: 250, image: "images/Luxury Penthouse.png" },
        { id: 6, name: "Beach House Villa", price: 180, image: "images/Beach house villas.png" }
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

// Generate amenity icons HTML
function generateAmenityIcons() {
    return [
        '<img src="images/icon_bed.png" alt="Bed" style="width: 20px; height: 20px; margin-right: 5px; vertical-align: middle;">Bed',
        '<img src="images/icon_bath.png" alt="Bath" style="width: 20px; height: 20px; margin-right: 5px; vertical-align: middle;">Bath',
        '<img src="images/icon_wifi.png" alt="WiFi" style="width: 20px; height: 20px; margin-right: 5px; vertical-align: middle;">WiFi'
    ];
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
    placeImage.src = place.image || 'images/icon.png';
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
                ${generateAmenityIcons().map(amenity => `<li>${amenity}</li>`).join('')}
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
            image: "images/Budget Hostel Room.png",
            host: "Sarah Johnson",
            location: "City Center",
            description: "A comfortable and affordable hostel room perfect for budget travelers. Clean facilities and friendly staff.",
            amenities: ["WiFi", "Shared Kitchen", "Lockers", "24/7 Reception"]
        },
        '2': {
            id: 2,
            name: "Shared Apartment",
            price: 45,
            image: "images/Shared Apartment.png",
            host: "Mike Chen",
            location: "Suburban Area",
            description: "A nice shared apartment with common areas and a great community atmosphere.",
            amenities: ["WiFi", "Kitchen", "Living Room", "Washing Machine"]
        },
        '3': {
            id: 3,
            name: "Cozy Downtown Apartment",
            price: 85,
            image: "images/Cozy Downtown Apartment.png",
            host: "John Doe",
            location: "Downtown Area",
            description: "A beautiful and cozy apartment located in the heart of downtown. Perfect for business travelers and tourists alike.",
            amenities: ["WiFi", "Air Conditioning", "Kitchen", "Parking", "TV", "Washing Machine"]
        },
        '4': {
            id: 4,
            name: "Modern Loft Space",
            price: 120,
            image: "images/Modern Loft Space.png",
            host: "Jane Smith",
            location: "Arts District",
            description: "A stylish modern loft with great city views and contemporary amenities.",
            amenities: ["WiFi", "Air Conditioning", "Kitchen", "Gym Access", "TV", "Balcony"]
        },
        '5': {
            id: 5,
            name: "Luxury Penthouse",
            price: 250,
            image: "images/Luxury Penthouse.png",
            host: "Robert Wilson",
            location: "Uptown",
            description: "An exclusive luxury penthouse with premium amenities and stunning views.",
            amenities: ["WiFi", "Air Conditioning", "Full Kitchen", "Private Pool", "Concierge", "Valet Parking"]
        },
        '6': {
            id: 6,
            name: "Beach House Villa",
            price: 180,
            image: "images/Beach house villas.png",
            host: "Maria Garcia",
            location: "Beachfront",
            description: "A beautiful beach house villa with direct beach access and ocean views.",
            amenities: ["WiFi", "Kitchen", "Beach Access", "BBQ Grill", "Outdoor Shower", "Parking"]
        }
    };
    
    const place = samplePlaces[placeId] || samplePlaces['1'];
    displayPlaceDetails(place);
    
    // Get stored reviews from localStorage and combine with sample reviews
    const storedReviews = JSON.parse(localStorage.getItem(`reviews_${placeId}`) || '[]');
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
    
    // Combine stored reviews (new ones first) with sample reviews
    const allReviews = [...storedReviews, ...sampleReviews];
    displayReviews(allReviews);
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

// Submit review with demo fallback
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
        
        // Demo fallback - simulate successful review submission
        if (rating && comment.trim()) {
            console.log('Using demo review submission');
            console.log(`Review submitted: ${rating} stars - ${comment}`);
            
            // Store review locally for demo purposes
            const newReview = {
                user_name: 'You', // In a real app, this would come from the authenticated user
                rating: parseInt(rating),
                comment: comment.trim(),
                date: new Date().toISOString()
            };
            
            // Get existing reviews from localStorage
            const existingReviews = JSON.parse(localStorage.getItem(`reviews_${placeId}`) || '[]');
            existingReviews.unshift(newReview); // Add new review at the beginning
            localStorage.setItem(`reviews_${placeId}`, JSON.stringify(existingReviews));
            
            return { success: true };
        }
        
        return { success: false, error: 'Please fill in all required fields.' };
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

// Handle add review page authentication and setup
function handleAddReviewPage() {
    // Check if user is authenticated, redirect to index if not
    const token = checkAuthenticationForAddReview();
    if (!token) {
        return; // Function will redirect automatically
    }
    
    // Update login/logout button for authenticated user
    const loginLink = document.getElementById('login-link');
    if (loginLink) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }
    
    // Get place ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id') || urlParams.get('id');
    
    if (!placeId) {
        showError('No place ID provided. Redirecting to home page...');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
        return;
    }
    
    // Load place name for the form
    loadPlaceNameForReview(placeId);
    
    // Setup back button
    const backButton = document.getElementById('back-to-place');
    if (backButton) {
        backButton.href = `place.html?id=${placeId}`;
    }
}

// Load place name for the add review form
async function loadPlaceNameForReview(placeId) {
    const placeNameInput = document.getElementById('place-name');
    if (!placeNameInput) return;
    
    try {
        const response = await makeAuthenticatedRequest(`${API_BASE_URL}/places/${placeId}`);
        
        if (response && response.ok) {
            const place = await response.json();
            placeNameInput.value = place.name;
        } else {
            // Fallback to sample data
            const samplePlaces = {
                '1': 'Budget Hostel Room',
                '2': 'Shared Apartment',
                '3': 'Cozy Downtown Apartment',
                '4': 'Modern Loft Space',
                '5': 'Luxury Penthouse',
                '6': 'Beach House Villa'
            };
            placeNameInput.value = samplePlaces[placeId] || 'Unknown Place';
        }
    } catch (error) {
        console.error('Error loading place name:', error);
        placeNameInput.value = 'Place Name Unavailable';
    }
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
            const placeId = urlParams.get('place_id') || urlParams.get('id') || '1'; // Default for demo
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
    
    // Handle add review page authentication and setup
    if (window.location.pathname.includes('add_review.html')) {
        handleAddReviewPage();
    }
    
    // Check authentication and load content based on page
    if (window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/')) {
        checkAuthenticationForIndex();
    } else if (window.location.pathname.includes('place.html')) {
        checkAuthenticationForPlace();
    }
});
