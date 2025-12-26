from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from functools import wraps

admin_bp = Blueprint('admin', __name__)

# Admin user IDs - in production, this should be in database or config
ADMIN_EMAILS = ['admin@college.edu']  # Add admin emails here

def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        
        if not user or user.email not in ADMIN_EMAILS:
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.route('/pending-users', methods=['GET'])
@admin_required
def get_pending_users():
    """Get all users pending verification"""
    try:
        user_type = request.args.get('user_type')
        
        query = User.query.filter_by(is_verified=False)
        
        if user_type:
            query = query.filter_by(user_type=user_type)
        
        pending_users = query.order_by(User.created_at.desc()).all()
        
        return jsonify({
            'count': len(pending_users),
            'users': [user.to_dict() for user in pending_users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/verify-user/<int:user_id>', methods=['PUT'])
@admin_required
def verify_user(user_id):
    """Verify a user account"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_verified = True
        db.session.commit()
        
        return jsonify({
            'message': 'User verified successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/reject-user/<int:user_id>', methods=['DELETE'])
@admin_required
def reject_user(user_id):
    """Reject and delete a user account"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.is_verified:
            return jsonify({'error': 'Cannot reject verified user'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User rejected and deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users with filters"""
    try:
        user_type = request.args.get('user_type')
        is_verified = request.args.get('is_verified')
        is_active = request.args.get('is_active')
        search = request.args.get('search')
        
        query = User.query
        
        if user_type:
            query = query.filter_by(user_type=user_type)
        if is_verified is not None:
            query = query.filter_by(is_verified=is_verified.lower() == 'true')
        if is_active is not None:
            query = query.filter_by(is_active=is_active.lower() == 'true')
        if search:
            query = query.filter(
                db.or_(
                    User.full_name.ilike(f'%{search}%'),
                    User.email.ilike(f'%{search}%'),
                    User.college_id.ilike(f'%{search}%')
                )
            )
        
        users = query.order_by(User.created_at.desc()).all()
        
        return jsonify({
            'count': len(users),
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/deactivate-user/<int:user_id>', methods=['PUT'])
@admin_required
def deactivate_user(user_id):
    """Deactivate a user account"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = False
        db.session.commit()
        
        return jsonify({
            'message': 'User deactivated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/activate-user/<int:user_id>', methods=['PUT'])
@admin_required
def activate_user(user_id):
    """Activate a user account"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = True
        db.session.commit()
        
        return jsonify({
            'message': 'User activated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/delete-user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Permanently delete a user account"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user is admin
        if user.email in ADMIN_EMAILS:
            return jsonify({'error': 'Cannot delete admin account'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_admin_stats():
    """Get platform statistics for admin dashboard"""
    try:
        stats = {
            'total_users': User.query.count(),
            'verified_users': User.query.filter_by(is_verified=True).count(),
            'pending_users': User.query.filter_by(is_verified=False).count(),
            'active_users': User.query.filter_by(is_active=True, is_verified=True).count(),
            'total_students': User.query.filter_by(user_type='student').count(),
            'total_alumni': User.query.filter_by(user_type='alumni').count(),
            'verified_students': User.query.filter_by(user_type='student', is_verified=True).count(),
            'verified_alumni': User.query.filter_by(user_type='alumni', is_verified=True).count(),
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/user/<int:user_id>', methods=['GET'])
@admin_required
def get_user_details(user_id):
    """Get detailed user information"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = user.to_dict()
        
        # Add additional statistics
        if user.user_type == 'alumni':
            user_data['jobs_posted_count'] = len(user.jobs_posted)
        else:
            user_data['applications_count'] = len(user.applications)
        
        user_data['messages_sent_count'] = len(user.messages_sent)
        user_data['messages_received_count'] = len(user.messages_received)
        
        return jsonify(user_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
