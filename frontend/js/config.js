// API Configuration
// Change this to your deployed backend URL when deploying to production
const API_CONFIG = {
    // For local development
    // BASE_URL: 'http://localhost:5000/api'

    // For production (replace with your Render backend URL)
    BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:5000/api'
        : 'https://YOUR-RENDER-APP-NAME.onrender.com/api'
};

// Export for use in other files
window.API_CONFIG = API_CONFIG;
