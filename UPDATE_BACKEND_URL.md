# After Deployment: Update Backend URL

After deploying your backend to Render, you need to update one file in the frontend.

## 📝 Steps

### 1. Get Your Render Backend URL

After deploying to Render, your backend URL will look like:
```
https://alumni-connect-backend-xyz.onrender.com
```

Copy this URL (without `/api` at the end)

### 2. Update Frontend Configuration

Open the file: `frontend/js/api.js`

Find these lines at the top:

```javascript
// API Configuration - automatically switches between local and production
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001/api'
    : 'https://YOUR-RENDER-APP-NAME.onrender.com/api'; // Update this with your Render backend URL
```

Replace `YOUR-RENDER-APP-NAME` with your actual Render app name.

For example, if your Render backend URL is:
```
https://alumni-connect-backend-abc.onrender.com
```

Update the line to:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001/api'
    : 'https://alumni-connect-backend-abc.onrender.com/api';
```

### 3. Commit and Push

```bash
git add frontend/js/api.js
git commit -m "Update backend URL for production"
git push
```

Netlify will automatically redeploy with the updated URL!

## ✅ That's It!

Your frontend will now connect to the correct backend:
- **Local development** → http://localhost:5001/api
- **Production (Netlify)** → Your Render backend URL

## 🧪 Test the Connection

Visit your Netlify site and:
1. Try registering a new user
2. Login as admin
3. If it works, you're done! 🎉

If you get CORS or connection errors:
- Double-check the URL in api.js
- Ensure backend is running on Render
- Check Render logs for errors
