# Deployment Guide - Alumni Connect System

This guide will walk you through deploying the Alumni Connect system with:
- **Frontend**: Netlify (Static Hosting)
- **Backend**: Render (Python Web Service with MySQL)

---

## 🎯 Prerequisites

1. **GitHub Account** - To push your code
2. **Netlify Account** - Sign up at https://netlify.com (free tier available)
3. **Render Account** - Sign up at https://render.com (free tier available)

---

## 📦 Part 1: Prepare Your Code

### 1.1 Initialize Git Repository (if not already done)

```bash
cd /Users/anuragdineshrokade/Alumini
git init
git add .
git commit -m "Initial commit - Alumni Connect System"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `alumni-connect`
3. **Do NOT initialize with README** (we already have code)
4. Click "Create repository"

### 1.3 Push Code to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/alumni-connect.git
git branch -M main
git push -u origin main
```

---

## 🚀 Part 2: Deploy Backend to Render

### 2.1 Create MySQL Database on Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → Select **"MySQL"**
3. Configure database:
   - **Name**: `alumniconnect-db`
   - **Database**: `alumniconnect`
   - **User**: `admin` (or your choice)
   - **Region**: Select nearest region
   - **Plan**: Free (or your choice)
4. Click **"Create Database"**
5. **IMPORTANT**: Copy the **Internal Database URL** (starts with `mysql://`)

### 2.2 Create Web Service on Render

1. In Render Dashboard, click **"New +"** → Select **"Web Service"**
2. Connect your GitHub repository:
   - **Repository**: `alumni-connect`
3. Configure the service:
   - **Name**: `alumni-connect-backend` (or your choice)
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free (or your choice)

### 2.3 Add Environment Variables

In the Render service settings, go to **"Environment"** tab and add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Paste the Internal Database URL from step 2.1 |
| `SECRET_KEY` | Click "Generate" or use: `your-secret-key-12345` |
| `JWT_SECRET_KEY` | Click "Generate" or use: `jwt-secret-key-12345` |
| `FLASK_ENV` | `production` |
| `PYTHON_VERSION` | `3.11.0` |

### 2.4 Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Once deployed, you'll see a URL like: `https://alumni-connect-backend.onrender.com`
4. **COPY THIS URL** - you'll need it for the frontend

### 2.5 Initialize Database

After deployment, go to the **Shell** tab in Render and run:

```bash
python
```

Then in Python shell:

```python
from app import app, db
from models import User

with app.app_context():
    db.create_all()
    
    # Create admin user
    admin = User(
        full_name='Admin User',
        email='admin@college.edu',
        college_id='ADMIN001',
        college_email='admin@college.edu',
        department='Administration',
        user_type='alumni',
        is_verified=True,
        is_active=True
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print("✅ Database initialized and admin user created!")

exit()
```

---

## 🌐 Part 3: Deploy Frontend to Netlify

### 3.1 Update Backend URL

1. Open `frontend/js/api.js`
2. Replace `YOUR-RENDER-APP-NAME` with your actual Render URL:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001/api'
    : 'https://alumni-connect-backend.onrender.com/api'; // ✅ Updated
```

3. Commit and push:

```bash
git add frontend/js/api.js
git commit -m "Update backend URL for production"
git push
```

### 3.2 Deploy to Netlify

**Option A: Netlify UI (Recommended)**

1. Go to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **GitHub** and select your `alumni-connect` repository
4. Configure build settings:
   - **Base directory**: `frontend`
   - **Publish directory**: `frontend` (leave empty or use `.`)
   - **Build command**: (leave empty)
5. Click **"Deploy site"**
6. Wait for deployment (1-2 minutes)
7. You'll get a URL like: `https://random-name-12345.netlify.app`

**Option B: Netlify CLI**

```bash
npm install -g netlify-cli
cd frontend
netlify deploy --prod
```

Follow the prompts and select `frontend` directory.

### 3.3 Custom Domain (Optional)

1. In Netlify Dashboard → **"Domain settings"**
2. Click **"Add custom domain"**
3. Follow instructions to connect your domain

---

## ✅ Part 4: Test Your Deployment

### 4.1 Test Backend

Visit: `https://your-backend.onrender.com/api/users/stats`

You should see JSON response (even if empty).

### 4.2 Test Frontend

1. Visit your Netlify URL
2. Click **"Register"**
3. Create a student account
4. Login as admin (`admin@college.edu` / `admin123`)
5. Verify the student
6. Login as student

---

## 🔧 Troubleshooting

### Backend Issues

**Issue**: 502 Bad Gateway
- **Solution**: Check Render logs, ensure DATABASE_URL is correct

**Issue**: Database connection error
- **Solution**: Verify MySQL database is running and URL is correct

### Frontend Issues

**Issue**: CORS errors
- **Solution**: Check backend CORS settings in `app.py`

**Issue**: Cannot connect to backend
- **Solution**: Verify API_BASE_URL in `frontend/js/api.js`

---

## 📝 Important Notes

1. **Free Tier Limits**:
   - Render free tier sleeps after 15 min inactivity (first request takes ~30s)
   - MySQL database on free tier has limited storage

2. **Security**:
   - Change default admin password immediately
   - Use strong SECRET_KEY and JWT_SECRET_KEY in production
   - Enable HTTPS (automatic on Netlify/Render)

3. **Costs**:
   - Netlify: Free for basic hosting
   - Render: Free tier available, paid plans start at $7/month

---

## 🎉 Your URLs

After deployment, save these:

- **Frontend**: `https://your-site.netlify.app`
- **Backend**: `https://your-backend.onrender.com`
- **Admin Login**: Use frontend URL + `/login.html`

---

## 📞 Support

If you encounter issues:
1. Check Render logs: Dashboard → Your Service → Logs
2. Check Netlify deploy logs: Dashboard → Deploys → View logs
3. Check browser console (F12) for frontend errors
