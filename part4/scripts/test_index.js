// Mock API and authentication for index feature testing
// API Configuration
const API_URL = 'http://localhost:5000/api';

// Global variable to store all places
let allPlaces = [];

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

// Check user authentication
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        loginLink.style.display = 'block';
        // Load sample places even without authentication for testing
        loadSamplePlaces();
    } else {
        loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
}

// Fetch places data from API
async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_URL}/places`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const places = await response.json();
            allPlaces = places;
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
            // Load sample data for demo purposes
            loadSamplePlaces();
        }
    } catch (error) {
        console.error('Error fetching places:', error);
        // Load sample data for demo purposes
        loadSamplePlaces();
    }
}

// Display places in the #places-list
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    
    // Clear the current content of the places list
    placesList.innerHTML = '';
    
    if (places.length === 0) {
        placesList.innerHTML = '<p class="text-center">No places found.</p>';
        return;
    }
    
    // Iterate over the places data
    places.forEach(place => {
        // For each place, create a div element and set its content
        const placeDiv = document.createElement('div');
        placeDiv.className = 'place-card';
        placeDiv.setAttribute('data-price', place.price_per_night || place.price || 0);
        
        // Use sample images for demo
        const imageUrl = getRandomImage();
        
        placeDiv.innerHTML = `
            <img src="${imageUrl}" alt="${place.name || place.title}" onerror="this.src='1.png'">
            <h3>${place.name || place.title}</h3>
            <p><strong>Description:</strong> ${place.description || 'A wonderful place to stay.'}</p>
            <p><strong>Location:</strong> ${place.city || place.location}, ${place.country}</p>
            <p><strong>Host:</strong> ${place.host?.first_name || place.host_name || 'Host'} ${place.host?.last_name || ''}</p>
            <p class="price">$${place.price_per_night || place.price}/night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        
        // Append the created element to the places list
        placesList.appendChild(placeDiv);
    });
}

// Get random image for demo purposes
function getRandomImage() {
    const images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png'];
    return images[Math.floor(Math.random() * images.length)];
}

// Load sample places for demo purposes
function loadSamplePlaces() {
    allPlaces = [
        {
            id: '1',
            name: 'Cozy Apartment in Paris',
            description: 'A charming apartment in the heart of Paris',
            city: 'Paris',
            country: 'France',
            price_per_night: 75,
            host: { first_name: 'Marie', last_name: 'Dubois' }
        },
        {
            id: '2',
            name: 'Modern Loft in New York',
            description: 'A stylish loft in Manhattan',
            city: 'New York',
            country: 'United States',
            price_per_night: 120,
            host: { first_name: 'John', last_name: 'Smith' }
        },
        {
            id: '3',
            name: 'Beach House in Barcelona',
            description: 'Beautiful house near the beach',
            city: 'Barcelona',
            country: 'Spain',
            price_per_night: 95,
            host: { first_name: 'Carlos', last_name: 'Rodriguez' }
        },
        {
            id: '4',
            name: 'Historic Villa in Rome',
            description: 'Historic villa with modern amenities',
            city: 'Rome',
            country: 'Italy',
            price_per_night: 85,
            host: { first_name: 'Giuseppe', last_name: 'Rossi' }
        },
        {
            id: '5',
            name: 'Budget Hostel Room',
            description: 'Affordable accommodation for backpackers',
            city: 'Berlin',
            country: 'Germany',
            price_per_night: 25,
            host: { first_name: 'Hans', last_name: 'Mueller' }
        },
        {
            id: '6',
            name: 'Luxury Penthouse',
            description: 'Luxurious penthouse with city views',
            city: 'Tokyo',
            country: 'Japan',
            price_per_night: 200,
            host: { first_name: 'Yuki', last_name: 'Tanaka' }
        }
    ];
    
    displayPlaces(allPlaces);
}

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', () => {
    const authStatus = document.getElementById('auth-status');
    const simulateLoginButton = document.getElementById('simulate-login');
    const clearAuthButton = document.getElementById('clear-auth');

    // Check user authentication on page load
    checkAuthentication();
    updateAuthStatus();

    if (simulateLoginButton) {
        simulateLoginButton.addEventListener('click', function() {
            setCookie('token', 'mock_jwt_token_' + new Date().getTime());
            checkAuthentication();
            updateAuthStatus();
        });
    }

    if (clearAuthButton) {
        clearAuthButton.addEventListener('click', function() {
            deleteCookie('token');
            checkAuthentication();
            updateAuthStatus();
        });
    }
    
    // Implement client-side filtering by price
    document.getElementById('price-filter').addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placeCards = document.querySelectorAll('.place-card');
        
        placeCards.forEach(card => {
            const placePrice = parseInt(card.getAttribute('data-price')) || 0;
            
            if (selectedPrice === 'all') {
                card.style.display = 'block';
            } else {
                const maxPrice = parseInt(selectedPrice);
                if (placePrice <= maxPrice) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            }
        });
    });

    function updateAuthStatus() {
        const token = getCookie('token');
        if (token) {
            authStatus.textContent = `✅ Authenticated with token: ${token.substring(0, 15)}...`;
        } else {
            authStatus.textContent = '❌ Not authenticated';
        }
    }
});
