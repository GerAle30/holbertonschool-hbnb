# HBNB Frontend - Part 4

This is the frontend implementation for the HBNB (Holberton AirBnB) project, featuring a complete web interface with login functionality, place listings, detailed views, and review management.

## Features

- **Login System**: JWT-based authentication with cookie storage
- **Place Listings**: Grid-based display of available places
- **Place Details**: Comprehensive information about places including amenities and reviews
- **Review System**: Add and view reviews for places (authenticated users only)
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: User-friendly error messages and form validation

## Files Structure

```
part4/
├── index.html          # Main page with place listings
├── login.html          # Login form
├── place.html          # Detailed place view with reviews
├── add_review.html     # Add review form
├── scripts.js          # Main JavaScript with API integration
├── css/
│   └── styles.css      # Main stylesheet
├── images/             # Image assets
│   ├── logo.png
│   ├── icon.png
│   ├── sample1.jpg
│   └── sample2.jpg
└── js/
    └── app.js          # Legacy JavaScript (replaced by scripts.js)
```

## API Integration

The frontend is configured to work with the HBNB backend API. Update the `API_BASE_URL` in `scripts.js` to match your backend server:

```javascript
const API_BASE_URL = 'http://localhost:5000/api/v1'; // Update this URL
```

### API Endpoints Used

- `POST /auth/login` - User authentication
- `GET /places` - Fetch all places
- `GET /places/{id}` - Fetch place details
- `GET /places/{id}/reviews` - Fetch place reviews
- `POST /places/{id}/reviews` - Add new review

## Authentication

The login system uses JWT tokens stored in browser cookies:

- Token is stored with 7-day expiration
- Automatic token validation on protected routes
- Automatic logout on token expiration
- UI updates based on authentication state

## Setup Instructions

1. **Start Backend Server**: Make sure your HBNB backend API is running
2. **Update API URL**: Modify `API_BASE_URL` in `scripts.js` if needed
3. **Serve Files**: Use a local web server to serve the files:

```bash
# Using Python's built-in server
python3 -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server

# Using PHP (if available)
php -S localhost:8000
```

4. **Access Application**: Open your browser to `http://localhost:8000`

## Usage

### Login
1. Navigate to `login.html` or click "Login" button
2. Enter valid credentials
3. Upon successful login, you'll be redirected to the main page
4. The login button will change to "Logout"

### Viewing Places
1. The main page displays available places in a grid layout
2. Each place card shows name, price, and "View Details" button
3. Click "View Details" to see full information

### Place Details
1. View comprehensive place information
2. See existing reviews from other users
3. If logged in, an "Add Review" button appears

### Adding Reviews
1. Must be logged in to add reviews
2. Click "Add Review" from place details page
3. Select rating (1-5 stars) and write comment
4. Submit to add review to the place

## Browser Compatibility

- Modern browsers with ES6+ support
- Chrome 60+
- Firefox 55+
- Safari 10.1+
- Edge 79+

## Error Handling

The application includes comprehensive error handling:

- Network connectivity issues
- API server errors
- Form validation
- Authentication failures
- Token expiration

## Security Features

- JWT token-based authentication
- HTTPS-ready (configure your server)
- XSS protection through proper data handling
- CSRF protection through token validation

## Development Notes

- The application gracefully falls back to sample data if the API is unavailable
- All forms include client-side validation
- Responsive design adapts to different screen sizes
- Authentication state persists across browser sessions

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your backend API allows requests from the frontend domain
2. **API Connection**: Verify the API_BASE_URL is correct and the backend is running
3. **Login Issues**: Check backend logs for authentication errors
4. **Missing Images**: Replace placeholder images with actual image files

### Debug Mode

Open browser developer tools to see console logs for debugging API calls and authentication state.

## W3C Validation

All HTML files are designed to pass W3C validation. Use the [W3C Markup Validator](https://validator.w3.org/) to verify.
