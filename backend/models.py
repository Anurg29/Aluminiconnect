from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    college_id = db.Column(db.String(50), nullable=False)
    college_email = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Enum('student', 'alumni'), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # For alumni
    passing_year = db.Column(db.Integer)
    current_company = db.Column(db.String(100))
    current_position = db.Column(db.String(100))
    bio = db.Column(db.Text)
    linkedin_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    
    # For students
    expected_passing_year = db.Column(db.Integer)
    current_year = db.Column(db.Integer)
    
    # Common fields
    profile_picture = db.Column(db.String(255))
    skills = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobs_posted = db.relationship('Job', backref='alumni', lazy=True, foreign_keys='Job.alumni_id')
    applications = db.relationship('Application', backref='student', lazy=True)
    messages_sent = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id')
    messages_received = db.relationship('Message', backref='receiver', lazy=True, foreign_keys='Message.receiver_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'college_id': self.college_id,
            'college_email': self.college_email,
            'department': self.department,
            'user_type': self.user_type,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'profile_picture': self.profile_picture,
            'skills': self.skills,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        
        if self.user_type == 'alumni':
            data.update({
                'passing_year': self.passing_year,
                'current_company': self.current_company,
                'current_position': self.current_position,
                'bio': self.bio,
                'linkedin_url': self.linkedin_url,
                'github_url': self.github_url,
            })
        else:
            data.update({
                'expected_passing_year': self.expected_passing_year,
                'current_year': self.current_year,
            })
        
        return data


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    job_type = db.Column(db.Enum('full-time', 'part-time', 'internship', 'contract'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary_range = db.Column(db.String(100))
    application_deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'alumni_id': self.alumni_id,
            'alumni_name': self.alumni.full_name if self.alumni else None,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'job_type': self.job_type,
            'description': self.description,
            'requirements': self.requirements,
            'salary_range': self.salary_range,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'applications_count': len(self.applications)
        }


class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    resume_path = db.Column(db.String(255))
    status = db.Column(db.Enum('pending', 'reviewed', 'shortlisted', 'rejected', 'accepted'), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else None,
            'student_id': self.student_id,
            'student_name': self.student.full_name if self.student else None,
            'student_email': self.student.email if self.student else None,
            'cover_letter': self.cover_letter,
            'resume_path': self.resume_path,
            'status': self.status,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
        }


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.full_name if self.sender else None,
            'receiver_id': self.receiver_id,
            'receiver_name': self.receiver.full_name if self.receiver else None,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user1 = db.relationship('User', foreign_keys=[user1_id])
    user2 = db.relationship('User', foreign_keys=[user2_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'user1_id': self.user1_id,
            'user1_name': self.user1.full_name if self.user1 else None,
            'user2_id': self.user2_id,
            'user2_name': self.user2.full_name if self.user2 else None,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
        }
