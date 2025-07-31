// Include auth utilities
document.head.appendChild(Object.assign(document.createElement('script'), {src: 'scripts/auth.js'}));

document.addEventListener('DOMContentLoaded', function() {
    // Check authentication - redirect to index if not authenticated
    if (!isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }

    const placeNameDiv = document.getElementById('place-name');
    const addReviewForm = document.getElementById('add-review-form');
    const messageDiv = document.getElementById('message');
    const backToPlaceLink = document.getElementById('back-to-place');

    // Get place ID from URL
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('place_id');

    if (!placeId) {
        window.location.href = 'index.html';
        return;
    }

    // Set back to place link
    backToPlaceLink.href = `place.html?id=${placeId}`;

    // Load place name
    loadPlaceName();

    // Add form submission handler
    addReviewForm.addEventListener('submit', submitReview);

    async function loadPlaceName() {
        try {
            const token = getToken();
            const response = await fetch(`${AUTH_API_URL}/places/${placeId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const place = await response.json();
                placeNameDiv.innerHTML = `<h2>Review for: ${place.name || place.title}</h2>`;
            } else {
                placeNameDiv.innerHTML = '<h2>Review for: Place</h2>';
            }

        } catch (error) {
            console.error('Error loading place name:', error);
            placeNameDiv.innerHTML = '<h2>Review for: Place</h2>';
        }
    }

    async function submitReview(e) {
        e.preventDefault();

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
            const submitButton = addReviewForm.querySelector('.submit-button');
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
                showMessage('Review submitted successfully! Redirecting...', 'success');
                
                // Redirect to place page after a short delay
                setTimeout(() => {
                    window.location.href = `place.html?id=${placeId}`;
                }, 2000);
                
            } else {
                const errorData = await response.json();
                showMessage(errorData.message || 'Failed to submit review. Please try again.', 'error');
            }

        } catch (error) {
            console.error('Error submitting review:', error);
            showMessage('Failed to submit review. Please check your connection and try again.', 'error');
        } finally {
            const submitButton = addReviewForm.querySelector('.submit-button');
            submitButton.textContent = 'Submit Review';
            submitButton.disabled = false;
        }
    }

    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
        messageDiv.classList.remove('hidden');
        
        // Hide message after 5 seconds (unless it's a success message)
        if (type !== 'success') {
            setTimeout(() => {
                messageDiv.classList.add('hidden');
            }, 5000);
        }
    }
});
