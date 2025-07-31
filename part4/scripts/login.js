// API Configuration
const API_URL = 'http://localhost:5000/api'; // Adjust this to your API URL

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

// Check if user is already authenticated
function isAuthenticated() {
    return getCookie('token') !== null;
}

// Login user function
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            // Store JWT token in cookie
            document.cookie = `token=${data.access_token}; path=/`;
            // Redirect to main page
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            alert('Login failed: ' + (errorData.message || response.statusText));
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Login failed: Network error. Please try again.');
    }
}

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', () => {
    // If already authenticated, redirect to index
    if (isAuthenticated()) {
        window.location.href = 'index.html';
        return;
    }

    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form data
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validate input
            if (!email || !password) {
                alert('Please enter both email and password.');
                return;
            }
            
            // Show loading state
            const submitButton = loginForm.querySelector('.submit-button');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Logging in...';
            submitButton.disabled = true;
            
            try {
                // Call login function
                await loginUser(email, password);
            } finally {
                // Reset button state
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        });
    }
});
