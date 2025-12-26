# 🚀 Render Deployment Guide - Step by Step

## ✅ Step 1: Create PostgreSQL Database (DO THIS FIRST)

### In Render Dashboard:

1. **Click "New +" button** (top right corner)
2. **Select "PostgreSQL"**
3. **Configure Database:**
   ```
   Name:     alumniconnect-db
   Database: alumniconnect
   User:     (keep default or use "admin")
   Region:   Oregon (or nearest to you)
   Plan:     Free
   ```
4. **Click "Create Database"**
5. **Wait 2-3 minutes** for provisioning
6. **IMPORTANT:** Once created, go to database dashboard and:
   - Find **"Internal Database URL"** in the "Connections" section
   - **COPY THIS URL** - it will look like:
     ```
     postgresql://admin:PASSWORD@HOST/alumniconnect
     ```
   - Save it somewhere - you'll need it in Step 2!

---

## ✅ Step 2: Create Web Service for Backend

### In Render Dashboard:

1. **Click "New +" button**
2. **Select "Web Service"**
3. **Connect GitHub Repository:**
   - Click "Connect account" if needed
   - Find and select: `Anurg29/Aluminiconnect`
   - Click "Connect"

4. **Configure Web Service:**
   ```
   Name:              alumniconnect-backend
   Region:            Same as database (Oregon recommended)
   Branch:            main
   Root Directory:    backend
   Runtime:           Python 3
   Build Command:     pip install -r requirements.txt
   Start Command:     gunicorn app:app
   Plan:              Free
   ```

5. **Scroll to "Environment Variables"** section

6. **Add Environment Variables** (Click "Add Environment Variable" for each):

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | Paste the Internal Database URL you copied from Step 1 |
   | `SECRET_KEY` | Click "Generate" or use: `alumniconnect-secret-2025` |
   | `JWT_SECRET_KEY` | Click "Generate" or use: `jwt-secret-2025` |
   | `FLASK_ENV` | `production` |
   | `PYTHON_VERSION` | `3.11.0` |

7. **Click "Create Web Service"**

8. **Wait 5-10 minutes** for deployment
   - You'll see build logs
   - Wait for "Deploy succeeded" message

9. **Copy Your Backend URL**
   - It will be like: `https://alumniconnect-backend-xyz.onrender.com`
   - **Save this URL** - you'll need it for frontend!

---

## ✅ Step 3: Initialize Database

### Once Backend is Deployed:

1. **In Render Dashboard**, go to your web service
2. **Click "Shell" tab** (in the left sidebar)
3. **Wait for shell to connect**
4. **Run these commands:**

   ```python
   python init_db.py
   ```

5. **You should see:**
   ```
   ✅ Database tables created successfully!
   ✅ Admin user created successfully!
   ==================================================
   Admin Credentials:
   Email: admin@college.edu
   Password: admin123
   ==================================================
   ```

6. **Done!** Your backend is now deployed with database!

---

## ✅ Step 4: Test Your Backend

### Visit these URLs (replace with your actual URL):

1. **Health Check:**
   ```
   https://your-app.onrender.com/api/health
   ```
   Should return: `{"status": "healthy"}`

2. **Stats Endpoint:**
   ```
   https://your-app.onrender.com/api/users/stats
   ```
   Should return JSON with stats

---

## 🎯 After Backend is Deployed

**You'll need your backend URL for the frontend deployment!**

Your backend URL format:
```
https://alumniconnect-backend-[random].onrender.com
```

**Update `frontend/js/api.js`** line 2-4 with this URL:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5001/api'
    : 'https://YOUR-ACTUAL-BACKEND-URL.onrender.com/api';
```

Then:
```bash
git add frontend/js/api.js
git commit -m "Update backend URL for production"
git push
```

---

## 🆘 Troubleshooting

### Build fails:
- Check build logs in Render
- Verify `requirements.txt` is correct
- Check Python version is 3.11

### Database connection error:
- Verify DATABASE_URL is correct
- Ensure database is running
- Check region matches

### 502 Bad Gateway after deploy:
- Check logs for errors
- May need to wait a minute for first start
- Free tier sleeps after 15 min (normal)

---

## ✅ Checklist

Before deploying frontend:

- [ ] Database created and running
- [ ] Web service deployed successfully
- [ ] init_db.py ran without errors
- [ ] Health check endpoint works
- [ ] Backend URL copied and saved

**Next: Deploy Frontend to Netlify!**
