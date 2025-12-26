# 🎓 Alumni Connect - College Alumni Management System

A comprehensive web-based Alumni Management System that connects students with alumni, facilitates job postings, enables messaging, and provides administrative controls.

![Status](https://img.shields.io/badge/status-ready%20for%20deployment-brightgreen)
![Backend](https://img.shields.io/badge/backend-Flask%20%2B%20MySQL-blue)
![Frontend](https://img.shields.io/badge/frontend-Vanilla%20JS%20%2B%20HTML%2FCSS-yellow)

---

## ✨ Features

### For Students
- ✅ **Registration & Verification** - Sign up and wait for admin approval
- 👥 **Alumni Directory** - Browse and connect with verified alumni
- 💼 **Job Portal** - Apply to job opportunities posted by alumni
- 💬 **Direct Messaging** - Chat with alumni one-on-one
- 📊 **Profile Management** - Update skills, projects, and personal information

### For Alumni
- ✅ **Registration & Verification** - Register with college credentials
- 📝 **Post Jobs** - Share job opportunities with students
- 💬 **Mentorship** - Connect with students through messaging
- 📊 **Profile Showcase** - Display current company, position, and achievements

### For Administrators
- 👤 **User Verification** - Approve/reject student and alumni registrations
- 📈 **Analytics Dashboard** - View platform statistics
- 🔒 **User Management** - Activate/deactivate accounts
- 🔍 **Search & Filter** - Find users by type, status, or keywords

---

## 🏗️ Tech Stack

### Backend
- **Framework**: Flask 3.0.0 (Python)
- **Database**: MySQL (Production) / SQLite (Local Development)
- **Authentication**: Flask-JWT-Extended
- **ORM**: SQLAlchemy
- **Server**: Gunicorn

### Frontend
- **Core**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Modern responsive UI with dark mode
- **API**: RESTful with JWT authentication

---

## 📁 Project Structure

```
Alumini/
├── backend/
│   ├── routes/               # API endpoints
│   │   ├── auth.py          # Authentication routes
│   │   ├── admin.py         # Admin routes
│   │   ├── users.py         # User management routes
│   │   ├── jobs.py          # Job posting routes
│   │   └── chat.py          # Messaging routes
│   ├── models.py            # Database models
│   ├── config.py            # Configuration
│   ├── app.py               # Application entry point
│   ├── init_db.py           # Database initialization script
│   ├── requirements.txt     # Python dependencies
│   ├── render.yaml          # Render deployment config
│   └── .env.example         # Environment variables template
│
├── frontend/
│   ├── js/
│   │   ├── api.js           # API client
│   │   ├── login.js         # Login logic
│   │   ├── register.js      # Registration logic
│   │   ├── admin.js         # Admin dashboard logic
│   │   └── home.js          # Homepage logic
│   ├── css/
│   │   ├── style.css        # Main styles
│   │   └── dashboard.css    # Dashboard styles
│   ├── index.html           # Landing page
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   └── admin-dashboard.html # Admin dashboard
│
├── DEPLOYMENT.md            # Detailed deployment guide
├── DEPLOY_CHECKLIST.md      # Quick deployment checklist
├── netlify.toml             # Netlify configuration
└── README.md                # This file
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- pip
- Modern web browser

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env
# Edit .env with your settings

# 6. Initialize database and create admin user
python init_db.py

# 7. Run the application
python app.py
```

The backend will be available at `http://localhost:5001`

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Open in browser
# Simply open index.html in your browser, or use a local server:
python -m http.server 8000

# Then visit: http://localhost:8000
```

---

## 🌐 Deployment

### Option 1: Quick Deploy (Recommended)

Follow the **[DEPLOY_CHECKLIST.md](./DEPLOY_CHECKLIST.md)** for a quick step-by-step guide.

### Option 2: Detailed Instructions

See **[DEPLOYMENT.md](./DEPLOYMENT.md)** for comprehensive deployment instructions including:
- GitHub setup
- Render deployment (Backend + MySQL)
- Netlify deployment (Frontend)
- Environment configuration
- Database initialization
- Troubleshooting

---

## 🔐 Default Credentials

After running `init_db.py`, you can login with:

- **Email**: `admin@college.edu`
- **Password**: `admin123`

⚠️ **IMPORTANT**: Change these credentials immediately after first login!

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/me` | Get current user |
| PUT | `/api/auth/update-profile` | Update profile |

### Admin Endpoints (Requires Admin Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/admin/pending-users` | Get pending verifications |
| PUT | `/api/admin/verify-user/:id` | Verify user |
| DELETE | `/api/admin/delete-user/:id` | Delete user |
| GET | `/api/admin/stats` | Get platform statistics |

### Job Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/jobs/` | List all jobs |
| POST | `/api/jobs/` | Create job (Alumni only) |
| GET | `/api/jobs/:id` | Get job details |
| POST | `/api/jobs/:id/apply` | Apply to job |

For complete API documentation, see `backend/README.md`

---

## 🧪 Testing

### Test Admin Approval Workflow

1. Start backend: `cd backend && python app.py`
2. Register a new student via frontend
3. Login as admin
4. Go to "Pending Users"
5. Verify the student
6. Login as the student

### Test Job Application Flow

1. Login as alumni
2. Post a job
3. Logout and login as student
4. Apply to the job
5. Check application status

---

## 🛠️ Environment Variables

### Backend (.env)

```env
DATABASE_URL=sqlite:///alumniconnect.db  # Or MySQL URL
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
```

For production, see `.env.example` for all available options.

---

## 📊 Database Schema

### Main Tables

- **users** - Student and alumni profiles
- **jobs** - Job postings
- **job_applications** - Job applications
- **messages** - Direct messages between users

See `backend/models.py` for complete schema.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🆘 Support & Troubleshooting

### Common Issues

**Backend not starting?**
- Check if port 5001 is available
- Verify virtual environment is activated
- Check .env file exists

**Database errors?**
- Run `python init_db.py` to initialize
- Check DATABASE_URL in .env

**CORS errors?**
- Verify CORS settings in `app.py`
- Check API_BASE_URL in `frontend/js/api.js`

**Admin can't login?**
- Run `python init_db.py` to create admin user
- Verify email: `admin@college.edu` password: `admin123`

### Getting Help

1. Check the [DEPLOYMENT.md](./DEPLOYMENT.md) guide
2. Review backend logs in terminal
3. Check browser console (F12) for frontend errors

---

## 🎯 Roadmap

- [ ] Email notifications for job applications
- [ ] Advanced search and filtering
- [ ] File upload for resumes
- [ ] Event management system
- [ ] Analytics dashboard for alumni
- [ ] Mobile responsive improvements
- [ ] Real-time messaging with WebSockets

---

## 👥 Authors

- **Anurag Dinesh Rokade** - Initial work

---

## 🙏 Acknowledgments

- Flask framework and community
- SQLAlchemy ORM
- JWT authentication libraries
- Netlify and Render for hosting

---

**Made with ❤️ for connecting students and alumni**
