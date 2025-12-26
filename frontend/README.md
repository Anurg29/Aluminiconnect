# AlumniConnect Frontend

Beautiful, modern frontend for the AlumniConnect platform, fully integrated with the Flask backend.

## Features

✨ **Modern Design**
- Clean, professional UI with gradient backgrounds
- Smooth animations and transitions
- Fully responsive design
- Icon-based feature cards

🔐 **Authentication**
- Student and Alumni registration
- Secure login with JWT tokens
- Profile management
- Password validation

📱 **Pages**
- Landing page with features
- Registration with student/alumni toggle
- Login with demo access
- Responsive navigation

🔌 **Backend Integration**
- Connected to Flask API at `localhost:5001`
- Complete API client library
- Error handling and loading states
- Auth token management

## File Structure

```
frontend/
├── index.html          # Landing page
├── login.html          # Login page
├── register.html       # Registration page
├── css/
│   └── style.css      # All styles
└── js/
    ├── api.js         # API client library
    ├── register.js    # Registration logic
    ├── login.js       # Login logic
    └── home.js        # Home page logic
```

## How to Use

### 1. Make sure backend is running:
```bash
cd ../backend
source venv/bin/activate
python app.py
```

Backend should be running at: `http://localhost:5001`

### 2. Open the frontend:

Simply open `index.html` in your browser:
```bash
open index.html
# or
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

### 3. Register an Account

1. Click "Register" or "Get Started"
2. Select "Student" or "Alumni"
3. Fill in the form with your details
4. Submit and wait for admin verification

### 4. Login

1. Use the email and password you registered with
2. If not verified yet, you'll get a message to wait
3. After admin verification, you can login successfully

## API Integration

The frontend connects to the backend using the `js/api.js` file:

```javascript
// Example usage:
// Register
await API.auth.register(userData);

// Login
await API.auth.login(email, password);

// Get alumni
await API.users.getAlumni();

// Get jobs
await API.jobs.getJobs();
```

## Design Highlights

- **Colors**: Purple/Blue gradients (#6366F1, #3B82F6)
- **Fonts**: Inter (Google Fonts fallback)
- **Icons**: Font Awesome 6
- **Animations**: Fade-in, slide-up, hover effects
- **Responsive**: Mobile-first approach

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Next Steps

After login, users will be redirected to:
- **Students/Alumni**: `dashboard.html` (to be created)
- **Admin**: `admin-dashboard.html` (to be created)

## Customization

Edit `css/style.css` to change:
- Colors (CSS variables at top)
- Fonts
- Spacing
- Animations

## Troubleshooting

**Backend not connecting?**
- Make sure Flask is running on port 5001
- Check browser console for CORS errors
- Verify API_BASE_URL in `js/api.js`

**Registration not working?**
- Check form validation
- Ensure all required fields are filled
- Check browser console for errors

## Demo

Visit the landing page to see:
- Animated hero section
- Feature cards with hover effects
- Live stats counter (from API)
- Smooth scroll animations

Enjoy! 🎉
