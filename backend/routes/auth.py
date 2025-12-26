from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import db, User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user (student or alumni)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'email', 'password', 'college_id', 
                          'college_email', 'department', 'user_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        if User.query.filter_by(college_email=data['college_email']).first():
            return jsonify({'error': 'College email already registered'}), 400
        
        # Create new user
        user = User(
            full_name=data['full_name'],
            email=data['email'],
            college_id=data['college_id'],
            college_email=data['college_email'],
            department=data['department'],
            user_type=data['user_type'],
            is_verified=False  # Admin needs to verify
        )
        
        user.set_password(data['password'])
        
        # Add type-specific fields
        if data['user_type'] == 'alumni':
            user.passing_year = data.get('passing_year')
            user.current_company = data.get('current_company')
            user.current_position = data.get('current_position')
            user.bio = data.get('bio')
            user.linkedin_url = data.get('linkedin_url')
            user.github_url = data.get('github_url')
        else:  # student
            user.expected_passing_year = data.get('expected_passing_year')
            user.current_year = data.get('current_year')
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful. Please wait for admin verification.',
            'user': user.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_verified:
            return jsonify({'error': 'Account not verified by admin yet'}), 403
        
        if not user.is_active:
            return jsonify({'error': 'Account has been deactivated'}), 403
        
        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=str(current_user_id))
        
        return jsonify({
            'access_token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update common fields
        updatable_fields = ['full_name', 'skills', 'profile_picture']
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        # Update type-specific fields
        if user.user_type == 'alumni':
            alumni_fields = ['current_company', 'current_position', 'bio', 
                           'linkedin_url', 'github_url']
            for field in alumni_fields:
                if field in data:
                    setattr(user, field, data[field])
        else:
            student_fields = ['current_year']
            for field in student_fields:
                if field in data:
                    setattr(user, field, data[field])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({'error': 'Old and new passwords are required'}), 400
        
        if not user.check_password(data['old_password']):
            return jsonify({'error': 'Incorrect old password'}), 401
        
        user.set_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
