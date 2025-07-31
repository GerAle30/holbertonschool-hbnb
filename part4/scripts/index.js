// Include auth utilities
document.head.appendChild(Object.assign(document.createElement('script'), {src: 'scripts/auth.js'}));

document.addEventListener('DOMContentLoaded', function() {
    // Check authentication - redirect to login if not authenticated
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }

    const placesContainer = document.getElementById('places-container');
    const countryFilter = document.getElementById('country-filter');
    let allPlaces = [];

    // Load places on page load
    loadPlaces();

    // Add country filter event listener
    countryFilter.addEventListener('change', filterPlaces);

    async function loadPlaces() {
        try {
            const token = getToken();
            const response = await fetch(`${AUTH_API_URL}/places`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                if (response.status === 401) {
                    // Token might be expired, redirect to login
                    logout();
                    return;
                }
                throw new Error('Failed to fetch places');
            }

            allPlaces = await response.json();
            displayPlaces(allPlaces);
            populateCountryFilter();

        } catch (error) {
            console.error('Error loading places:', error);
            // For demo purposes, load sample data
            loadSamplePlaces();
        }
    }


    function displayPlaces(places) {
        placesContainer.innerHTML = '';

        if (places.length === 0) {
            placesContainer.innerHTML = '<p class="text-center">No places found.</p>';
            return;
        }

        places.forEach(place => {
            const placeCard = createPlaceCard(place);
            placesContainer.appendChild(placeCard);
        });
    }

    function createPlaceCard(place) {
        const card = document.createElement('div');
        card.className = 'place-card';
        
        // Use sample images for demo
        const imageUrl = getRandomImage();
        
        card.innerHTML = `
            <img src="${imageUrl}" alt="${place.name || place.title}" onerror="this.src='1.png'">
            <h3>${place.name || place.title}</h3>
            <p><strong>Location:</strong> ${place.city || place.location}, ${place.country}</p>
            <p><strong>Host:</strong> ${place.host?.first_name || place.host_name || 'Host'} ${place.host?.last_name || ''}</p>
            <p class="price">$${place.price_per_night || place.price}/night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        
        return card;
    }

    function getRandomImage() {
        const images = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png'];
        return images[Math.floor(Math.random() * images.length)];
    }

    function populateCountryFilter() {
        // Get unique countries from places
        const countries = [...new Set(allPlaces.map(place => place.country))];
        
        // Clear existing options except "All Countries"
        const allOption = countryFilter.firstElementChild;
        countryFilter.innerHTML = '';
        countryFilter.appendChild(allOption);
        
        // Add country options
        countries.forEach(country => {
            if (country) {
                const option = document.createElement('option');
                option.value = country;
                option.textContent = country;
                countryFilter.appendChild(option);
            }
        });
    }

    function filterPlaces() {
        const selectedCountry = countryFilter.value;
        
        if (!selectedCountry) {
            displayPlaces(allPlaces);
        } else {
            const filteredPlaces = allPlaces.filter(place => place.country === selectedCountry);
            displayPlaces(filteredPlaces);
        }
    }

    // Sample data for demo purposes
    function loadSamplePlaces() {
        allPlaces = [
            {
                id: '1',
                name: 'Cozy Apartment in Paris',
                city: 'Paris',
                country: 'France',
                price_per_night: 120,
                host: { first_name: 'Marie', last_name: 'Dubois' }
            },
            {
                id: '2',
                name: 'Modern Loft in New York',
                city: 'New York',
                country: 'United States',
                price_per_night: 200,
                host: { first_name: 'John', last_name: 'Smith' }
            },
            {
                id: '3',
                name: 'Beach House in Barcelona',
                city: 'Barcelona',
                country: 'Spain',
                price_per_night: 150,
                host: { first_name: 'Carlos', last_name: 'Rodriguez' }
            },
            {
                id: '4',
                name: 'Historic Villa in Rome',
                city: 'Rome',
                country: 'Italy',
                price_per_night: 180,
                host: { first_name: 'Giuseppe', last_name: 'Rossi' }
            },
            {
                id: '5',
                name: 'Countryside Cottage in London',
                city: 'London',
                country: 'United Kingdom',
                price_per_night: 140,
                host: { first_name: 'Emma', last_name: 'Thompson' }
            }
        ];
        
        displayPlaces(allPlaces);
        populateCountryFilter();
    }
});
