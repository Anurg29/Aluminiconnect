# 🚀 Quick Deployment Checklist

## ✅ Pre-Deployment (Done)

- [x] Unnecessary files removed (venv, __pycache__, .db files)
- [x] Backend configured for MySQL
- [x] Frontend API URL configured for environment switching
- [x] requirements.txt includes gunicorn and psycopg2-binary
- [x] Netlify configuration created (netlify.toml)
- [x] Render configuration created (render.yaml)

## 📋 Deployment Steps

### 1️⃣ Push to GitHub
```bash
cd /Users/anuragdineshrokade/Alumini
git init
git add .
git commit -m "Initial commit - Alumni Connect System"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/alumni-connect.git
git branch -M main
git push -u origin main
```

### 2️⃣ Deploy Backend to Render

1. **Create MySQL Database**
   - Go to https://dashboard.render.com
   - New + → MySQL
   - Name: `alumniconnect-db`
   - Copy the Internal Database URL

2. **Create Web Service**
   - New + → Web Service
   - Connect GitHub repo: `alumni-connect`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add Environment Variables**
   - `DATABASE_URL`: (paste MySQL URL)
   - `SECRET_KEY`: (generate or use strong key)
   - `JWT_SECRET_KEY`: (generate or use strong key)
   - `FLASK_ENV`: `production`

4. **Initialize Database**
   - Use Render Shell to run Python and create tables
   - Create admin user
   - Copy your Render backend URL

### 3️⃣ Update Frontend

1. **Edit `frontend/js/api.js`**
   - Replace `YOUR-RENDER-APP-NAME` with your actual Render app name
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
       ? 'http://localhost:5001/api'
       : 'https://YOUR-ACTUAL-NAME.onrender.com/api';
   ```

2. **Commit and Push**
   ```bash
   git add frontend/js/api.js
   git commit -m "Update backend URL"
   git push
   ```

### 4️⃣ Deploy Frontend to Netlify

1. **Deploy via Netlify Dashboard**
   - Go to https://app.netlify.com
   - Add new site → Import from GitHub
   - Select: `alumni-connect` repository
   - Base directory: `frontend`
   - Click Deploy

2. **Copy your Netlify URL**
   - Will be like: `https://random-name.netlify.app`

### 5️⃣ Test Deployment

- [ ] Visit frontend URL
- [ ] Register a new student
- [ ] Login as admin (admin@college.edu / admin123)
- [ ] Verify the student
- [ ] Login as the student
- [ ] Test features (jobs, chat, profile)

## 🎯 Your Deployment URLs

Write them here after deployment:

- **Frontend (Netlify)**: _______________________________
- **Backend (Render)**: _______________________________
- **MySQL Database**: _______________________________

## 🔐 Admin Credentials

- **Email**: admin@college.edu
- **Password**: admin123
- ⚠️ **Change this immediately after first login!**

## 🆘 Quick Fixes

**Backend not responding?**
- Check Render logs
- Verify DATABASE_URL is correct
- Free tier sleeps after 15min (first request slow)

**CORS errors?**
- Verify backend CORS settings in app.py
- Check API_BASE_URL in frontend

**Database errors?**
- Run database initialization script
- Check MySQL connection

---

**📖 For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)**
