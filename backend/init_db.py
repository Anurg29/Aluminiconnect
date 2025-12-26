"""
Database initialization script for production deployment.
Run this in Render Shell after deploying the backend.
"""

from app import app, db
from models import User

def init_database():
    """Initialize database tables and create admin user"""
    with app.app_context():
        try:
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if admin already exists
            existing_admin = User.query.filter_by(email='admin@college.edu').first()
            if existing_admin:
                print("ℹ️  Admin user already exists. Skipping creation.")
                return
            
            # Create admin user
            print("Creating admin user...")
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
            
            print("✅ Admin user created successfully!")
            print("=" * 50)
            print("Admin Credentials:")
            print("Email: admin@college.edu")
            print("Password: admin123")
            print("⚠️  IMPORTANT: Change the password after first login!")
            print("=" * 50)
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    init_database()
