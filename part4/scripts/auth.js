// Authentication utilities
const AUTH_API_URL = 'http://localhost:5000/api'; // Adjust this to your API URL

// Cookie utilities
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

// Check if user is authenticated
function isAuthenticated() {
    return getCookie('token') !== null;
}

// Get the current user token
function getToken() {
    return getCookie('token');
}

// Logout function
function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

// Update login button based on authentication status
function updateLoginButton() {
    const loginLink = document.getElementById('login-link');
    if (isAuthenticated()) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.onclick = function(e) {
            e.preventDefault();
            logout();
        };
    } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
        loginLink.onclick = null;
    }
}

// Check authentication and redirect if needed
function checkAuthAndRedirect(redirectTo = 'login.html') {
    if (!isAuthenticated()) {
        window.location.href = redirectTo;
        return false;
    }
    return true;
}

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', function() {
    updateLoginButton();
});
