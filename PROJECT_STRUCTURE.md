# 🎓 Alumni Connect - Project Structure

```
Alumini/
│
├── 📁 backend/                      # Flask Backend API
│   ├── 📁 routes/                   # API route handlers
│   │   ├── admin.py                # Admin management endpoints
│   │   ├── auth.py                 # Authentication endpoints
│   │   ├── chat.py                 # Messaging endpoints
│   │   ├── jobs.py                 # Job posting endpoints
│   │   └── users.py                # User management endpoints
│   │
│   ├── app.py                      # Main Flask application
│   ├── config.py                   # Configuration settings
│   ├── models.py                   # Database models (SQLAlchemy)
│   ├── init_db.py                  # Database initialization script
│   ├── requirements.txt            # Python dependencies
│   ├── runtime.txt                 # Python version for deployment
│   ├── render.yaml                 # Render deployment configuration
│   ├── .env                        # Environment variables (MySQL connection)
│   ├── .env.example                # Environment template
│   ├── .gitignore                  # Git ignore rules
│   └── README.md                   # Backend documentation
│
├── 📁 frontend/                     # Static Frontend
│   ├── 📁 css/                     # Stylesheets
│   │   ├── style.css               # Main styles
│   │   └── dashboard.css           # Dashboard styles
│   │
│   ├── 📁 js/                      # JavaScript files
│   │   ├── api.js                  # API client & utilities
│   │   ├── admin.js                # Admin dashboard logic
│   │   ├── login.js                # Login page logic
│   │   ├── register.js             # Registration logic
│   │   └── home.js                 # Homepage logic
│   │
│   ├── index.html                  # Landing page
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── admin-dashboard.html        # Admin dashboard
│   ├── .gitignore                  # Git ignore rules
│   └── README.md                   # Frontend documentation
│
├── README.md                        # Main project documentation
├── DEPLOYMENT.md                    # Deployment guide (Netlify + Render)
├── netlify.toml                    # Netlify configuration
└── .gitignore                      # Root git ignore rules

```

## 📊 Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database**: MySQL 9.5.0 (Local) / MySQL (Production)
- **ORM**: SQLAlchemy 3.1.1
- **Authentication**: JWT (Flask-JWT-Extended 4.5.3)
- **Libraries**: PyMySQL, Flask-CORS, python-dotenv

### Frontend
- **Core**: HTML5, CSS3, Vanilla JavaScript
- **Design**: Modern responsive UI with gradients
- **API**: RESTful with JWT authentication

## 🗄️ Database Schema

**Tables:**
- `users` - Student & alumni profiles
- `jobs` - Job postings by alumni
- `applications` - Student job applications
- `messages` - Direct messages
- `conversations` - Chat conversations

## 🚀 Quick Start

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

### Frontend
Simply open `frontend/index.html` in a browser or use:
```bash
cd frontend
python -m http.server 8000
```

## 📝 Environment Variables

Create `backend/.env`:
```env
DATABASE_URL=mysql+pymysql://root@localhost:3306/alumniconnect
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🔐 Default Admin Credentials
- Email: `admin@college.edu`
- Password: `admin123`

## 📚 Documentation
- [README.md](./README.md) - Project overview
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide
- [backend/README.md](./backend/README.md) - API documentation
- [frontend/README.md](./frontend/README.md) - Frontend guide
