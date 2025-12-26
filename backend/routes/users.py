from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from sqlalchemy import or_

users_bp = Blueprint('users', __name__)

@users_bp.route('/alumni', methods=['GET'])
@jwt_required()
def get_alumni():
    """Get all verified alumni"""
    try:
        # Get query parameters for filtering
        department = request.args.get('department')
        company = request.args.get('company')
        passing_year = request.args.get('passing_year')
        search = request.args.get('search')
        
        # Base query
        query = User.query.filter_by(user_type='alumni', is_verified=True, is_active=True)
        
        # Apply filters
        if department:
            query = query.filter_by(department=department)
        if company:
            query = query.filter(User.current_company.ilike(f'%{company}%'))
        if passing_year:
            query = query.filter_by(passing_year=int(passing_year))
        if search:
            query = query.filter(
                or_(
                    User.full_name.ilike(f'%{search}%'),
                    User.current_company.ilike(f'%{search}%'),
                    User.current_position.ilike(f'%{search}%')
                )
            )
        
        alumni = query.all()
        
        return jsonify({
            'count': len(alumni),
            'alumni': [a.to_dict() for a in alumni]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """Get all verified students"""
    try:
        # Get query parameters for filtering
        department = request.args.get('department')
        year = request.args.get('year')
        search = request.args.get('search')
        
        # Base query
        query = User.query.filter_by(user_type='student', is_verified=True, is_active=True)
        
        # Apply filters
        if department:
            query = query.filter_by(department=department)
        if year:
            query = query.filter_by(current_year=int(year))
        if search:
            query = query.filter(User.full_name.ilike(f'%{search}%'))
        
        students = query.all()
        
        return jsonify({
            'count': len(students),
            'students': [s.to_dict() for s in students]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    """Get specific user profile by ID"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_verified or not user.is_active:
            return jsonify({'error': 'User profile not available'}), 403
        
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    """Get all unique departments"""
    try:
        departments = db.session.query(User.department).distinct().all()
        departments_list = [d[0] for d in departments if d[0]]
        
        return jsonify({
            'departments': sorted(departments_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@users_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get platform statistics"""
    try:
        total_alumni = User.query.filter_by(user_type='alumni', is_verified=True, is_active=True).count()
        total_students = User.query.filter_by(user_type='student', is_verified=True, is_active=True).count()
        
        return jsonify({
            'total_alumni': total_alumni,
            'total_students': total_students,
            'total_users': total_alumni + total_students
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
