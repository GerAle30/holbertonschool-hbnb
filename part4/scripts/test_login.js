// Mock API Configuration for testing
const MOCK_API_URL = 'http://localhost:5000/api';

// Cookie utility functions (same as in login.js)
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

// Check if user is already authenticated
function isAuthenticated() {
    return getCookie('token') !== null;
}

// Mock login function for testing
async function mockLoginUser(email, password) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // Simulate API response
            if (email === 'user@example.com' && password === 'password123') {
                resolve({
                    ok: true,
                    json: () => Promise.resolve({
                        access_token: 'mock_jwt_token_' + new Date().getTime(),
                        user: {
                            id: 1,
                            email: email,
                            first_name: 'John',
                            last_name: 'Doe'
                        }
                    })
                });
            } else {
                resolve({
                    ok: false,
                    statusText: 'Unauthorized',
                    json: () => Promise.resolve({
                        message: 'Invalid email or password'
                    })
                });
            }
        }, 1000); // Simulate network delay
    });
}

// Test login user function
async function testLoginUser(email, password) {
    try {
        showMessage('Attempting login...', 'info');
        
        // Use mock API for testing
        const response = await mockLoginUser(email, password);
        
        if (response.ok) {
            const data = await response.json();
            // Store JWT token in cookie
            document.cookie = `token=${data.access_token}; path=/`;
            showMessage('Login successful! Token stored in cookie.', 'success');
            updateAuthStatus();
            
            // Simulate redirect after delay
            setTimeout(() => {
                showMessage('Redirecting to index.html...', 'info');
                // Uncomment the next line to actually redirect
                // window.location.href = 'index.html';
            }, 2000);
        } else {
            const errorData = await response.json();
            showMessage('Login failed: ' + (errorData.message || response.statusText), 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('Login failed: Network error. Please try again.', 'error');
    }
}

function updateAuthStatus() {
    const authStatus = document.getElementById('auth-status');
    const token = getCookie('token');
    
    if (token) {
        authStatus.innerHTML = `
            <strong>Status:</strong> Authenticated<br>
            <strong>Token:</strong> ${token.substring(0, 20)}...
        `;
    } else {
        authStatus.innerHTML = '<strong>Status:</strong> Not authenticated';
    }
}

function showMessage(message, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.className = type === 'success' ? 'success-message' : 
                          type === 'error' ? 'error-message' : 'info-message';
    messageDiv.classList.remove('hidden');
    
    // Hide message after 5 seconds for non-success messages
    if (type !== 'success') {
        setTimeout(() => {
            messageDiv.classList.add('hidden');
        }, 5000);
    }
}

// DOM Content Loaded Event Listener
document.addEventListener('DOMContentLoaded', () => {
    const testLoginForm = document.getElementById('test-login-form');
    const checkTokenBtn = document.getElementById('check-token');
    const clearTokenBtn = document.getElementById('clear-token');
    
    // Update auth status on page load
    updateAuthStatus();
    
    // Test login form submission
    if (testLoginForm) {
        testLoginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form data
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validate input
            if (!email || !password) {
                showMessage('Please enter both email and password.', 'error');
                return;
            }
            
            // Show loading state
            const submitButton = testLoginForm.querySelector('.submit-button');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Testing Login...';
            submitButton.disabled = true;
            
            try {
                // Call test login function
                await testLoginUser(email, password);
            } finally {
                // Reset button state
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        });
    }
    
    // Check token button
    if (checkTokenBtn) {
        checkTokenBtn.addEventListener('click', () => {
            updateAuthStatus();
            showMessage('Authentication status updated.', 'info');
        });
    }
    
    // Clear token button
    if (clearTokenBtn) {
        clearTokenBtn.addEventListener('click', () => {
            deleteCookie('token');
            updateAuthStatus();
            showMessage('Token cleared successfully.', 'success');
        });
    }
});

// Add info message style to CSS if not present
const style = document.createElement('style');
style.textContent = `
    .info-message {
        color: #3498db;
        margin-top: 10px;
        padding: 10px;
        background-color: #f0f8ff;
        border: 1px solid #3498db;
        border-radius: 5px;
    }
`;
document.head.appendChild(style);
