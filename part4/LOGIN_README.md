# HBnB Login Functionality

## Overview

This implementation provides complete login functionality for the HBnB application following the specified requirements.

## Features

✅ **Event Listener Setup**: Form submission handled with `preventDefault()`  
✅ **AJAX Request**: Uses Fetch API with proper headers and JSON body  
✅ **JWT Token Storage**: Stores token in cookies for session management  
✅ **Success Handling**: Redirects to index.html on successful login  
✅ **Error Handling**: Displays appropriate error messages on failure  

## Files Structure

```
part4/
├── login.html              # Login form page
├── test_login.html         # Test page with mock API
├── scripts/
│   ├── login.js            # Main login functionality
│   ├── test_login.js       # Test implementation with mock API
│   └── auth.js             # Authentication utilities
├── styles.css              # Styling for all pages
└── LOGIN_README.md         # This documentation
```

## Implementation Details

### 1. Event Listener Setup
```javascript
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Handle form submission
        });
    }
});
```

### 2. AJAX Request to API
```javascript
async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    // Handle response...
}
```

### 3. JWT Token Storage
```javascript
if (response.ok) {
    const data = await response.json();
    // Store JWT token in cookie
    document.cookie = `token=${data.access_token}; path=/`;
    // Redirect to main page
    window.location.href = 'index.html';
}
```

### 4. Error Handling
```javascript
if (!response.ok) {
    const errorData = await response.json();
    alert('Login failed: ' + (errorData.message || response.statusText));
}
```

### 5. Cookie Utilities
- `setCookie(name, value, days)` - Store data in cookies
- `getCookie(name)` - Retrieve data from cookies
- `isAuthenticated()` - Check if user has valid token

## Testing

### Option 1: Test with Mock API
1. Open `test_login.html` in your browser
2. Use test credentials:
   - **Email**: user@example.com
   - **Password**: password123
3. Click "Test Login" to simulate the login process
4. Check authentication status and token storage

### Option 2: Test with Real API
1. Ensure your API server is running on `http://localhost:5000`
2. Update the `API_URL` in `login.js` if needed
3. Open `login.html` in your browser
4. Enter valid credentials and test login

## API Configuration

The API URL is configurable in `login.js`:
```javascript
const API_URL = 'http://localhost:5000/api'; // Adjust this to your API URL
```

## Expected API Response

**Success Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

**Error Response:**
```json
{
    "message": "Invalid email or password"
}
```

## Security Considerations

- JWT tokens are stored in cookies with proper path settings
- Form validation prevents empty submissions
- Error handling prevents sensitive information exposure
- HTTPS should be used in production environments

## Browser Compatibility

- Modern browsers supporting ES6+ features
- Fetch API support required
- Cookie support required for session management

## Troubleshooting

### Common Issues:

1. **CORS Errors**: Configure your API to allow cross-origin requests
2. **Network Errors**: Check API URL and server availability
3. **Cookie Issues**: Ensure proper domain/path settings
4. **Token Not Stored**: Check browser console for JavaScript errors

### Debug Steps:
1. Open browser developer tools
2. Check Network tab for API requests
3. Check Application tab for cookie storage
4. Check Console for JavaScript errors
