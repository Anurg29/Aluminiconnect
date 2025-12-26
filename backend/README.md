# AlumniConnect Backend

Flask-based REST API for AlumniConnect platform connecting students and alumni.

## Features

✅ **User Management**
- Student and Alumni registration with college ID verification
- Admin verification system
- Profile management

✅ **Job Portal**
- Alumni can post job opportunities
- Students can apply to jobs
- Application tracking and status management

✅ **Messaging System**
- Direct chat between students and alumni
- Conversation management
- Unread message tracking

✅ **Admin Dashboard**
- User verification and management
- Account activation/deactivation
- Platform statistics

## Tech Stack

- **Framework**: Flask 3.0
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (Flask-JWT-Extended)
- **CORS**: Flask-CORS

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server

### Steps

1. **Clone and navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL Database**
   ```bash
   mysql -u root -p
   ```
   ```sql
   CREATE DATABASE alumniconnect;
   EXIT;
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - Login user
- `POST /refresh` - Refresh access token
- `GET /me` - Get current user
- `PUT /update-profile` - Update profile
- `POST /change-password` - Change password

### Users (`/api/users`)
- `GET /alumni` - Get all alumni
- `GET /students` - Get all students
- `GET /<id>` - Get user profile
- `GET /departments` - Get departments
- `GET /stats` - Get statistics

### Jobs (`/api/jobs`)
- `GET /` - Get all jobs
- `POST /` - Create job (alumni only)
- `GET /<id>` - Get job details
- `PUT /<id>` - Update job
- `DELETE /<id>` - Delete job
- `POST /<id>/apply` - Apply to job (students only)
- `GET /my-jobs` - Get my posted jobs
- `GET /my-applications` - Get my applications
- `GET /<id>/applications` - Get job applications
- `PUT /applications/<id>/status` - Update application status

### Chat (`/api/chat`)
- `GET /conversations` - Get conversations
- `GET /messages/<user_id>` - Get messages with user
- `POST /send` - Send message
- `PUT /mark-read/<id>` - Mark message as read
- `GET /unread-count` - Get unread count
- `DELETE /delete/<id>` - Delete message

### Admin (`/api/admin`)
- `GET /pending-users` - Get pending verifications
- `PUT /verify-user/<id>` - Verify user
- `DELETE /reject-user/<id>` - Reject user
- `GET /users` - Get all users
- `PUT /deactivate-user/<id>` - Deactivate user
- `PUT /activate-user/<id>` - Activate user
- `DELETE /delete-user/<id>` - Delete user
- `GET /stats` - Get admin statistics
- `GET /user/<id>` - Get user details

## Database Schema

### Users Table
- id, full_name, email, password_hash
- college_id, college_email, department
- user_type (student/alumni)
- is_verified, is_active
- Alumni: passing_year, current_company, current_position, bio, linkedin_url, github_url
- Student: expected_passing_year, current_year

### Jobs Table
- id, alumni_id, title, company, location
- job_type, description, requirements
- salary_range, application_deadline
- is_active, created_at, updated_at

### Applications Table
- id, job_id, student_id
- cover_letter, resume_path
- status (pending/reviewed/shortlisted/rejected/accepted)
- applied_at, updated_at

### Messages Table
- id, sender_id, receiver_id
- content, is_read, created_at

### Conversations Table
- id, user1_id, user2_id
- last_message_at, created_at

## Configuration

Edit `.env` file:
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=alumniconnect
```

## Admin Setup

Add admin emails in `routes/admin.py`:
```python
ADMIN_EMAILS = ['admin@college.edu']
```

## Testing

Use tools like Postman or curl to test API endpoints:

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"full_name":"John Doe","email":"john@example.com","password":"password123","college_id":"CS2023001","college_email":"john@college.edu","department":"Computer Science","user_type":"student","expected_passing_year":2027,"current_year":1}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}'
```

## License

MIT License
