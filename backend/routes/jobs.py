from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Job, Application, User
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/', methods=['GET'])
@jwt_required()
def get_jobs():
    """Get all active job postings"""
    try:
        # Get query parameters for filtering
        job_type = request.args.get('job_type')
        company = request.args.get('company')
        location = request.args.get('location')
        search = request.args.get('search')
        
        # Base query
        query = Job.query.filter_by(is_active=True)
        
        # Apply filters
        if job_type:
            query = query.filter_by(job_type=job_type)
        if company:
            query = query.filter(Job.company.ilike(f'%{company}%'))
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        if search:
            query = query.filter(
                db.or_(
                    Job.title.ilike(f'%{search}%'),
                    Job.description.ilike(f'%{search}%')
                )
            )
        
        jobs = query.order_by(Job.created_at.desc()).all()
        
        return jsonify({
            'count': len(jobs),
            'jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/', methods=['POST'])
@jwt_required()
def create_job():
    """Create a new job posting (alumni only)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.user_type != 'alumni':
            return jsonify({'error': 'Only alumni can post jobs'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'company', 'job_type', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new job
        job = Job(
            alumni_id=current_user_id,
            title=data['title'],
            company=data['company'],
            location=data.get('location'),
            job_type=data['job_type'],
            description=data['description'],
            requirements=data.get('requirements'),
            salary_range=data.get('salary_range')
        )
        
        # Parse application deadline if provided
        if data.get('application_deadline'):
            try:
                job.application_deadline = datetime.fromisoformat(data['application_deadline'])
            except ValueError:
                return jsonify({'error': 'Invalid date format for application_deadline'}), 400
        
        db.session.add(job)
        db.session.commit()
        
        return jsonify({
            'message': 'Job posted successfully',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get specific job details"""
    try:
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Update job posting (only by the alumni who posted it)"""
    try:
        current_user_id = get_jwt_identity()
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        if job.alumni_id != current_user_id:
            return jsonify({'error': 'Unauthorized to update this job'}), 403
        
        data = request.get_json()
        
        # Update fields
        updatable_fields = ['title', 'company', 'location', 'job_type', 
                           'description', 'requirements', 'salary_range', 'is_active']
        for field in updatable_fields:
            if field in data:
                setattr(job, field, data[field])
        
        # Update deadline if provided
        if 'application_deadline' in data:
            try:
                job.application_deadline = datetime.fromisoformat(data['application_deadline'])
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Job updated successfully',
            'job': job.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Delete job posting (only by the alumni who posted it)"""
    try:
        current_user_id = get_jwt_identity()
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        if job.alumni_id != current_user_id:
            return jsonify({'error': 'Unauthorized to delete this job'}), 403
        
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<int:job_id>/apply', methods=['POST'])
@jwt_required()
def apply_to_job(job_id):
    """Apply to a job posting (students only)"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.user_type != 'student':
            return jsonify({'error': 'Only students can apply to jobs'}), 403
        
        job = Job.query.get(job_id)
        if not job or not job.is_active:
            return jsonify({'error': 'Job not found or inactive'}), 404
        
        # Check if already applied
        existing_application = Application.query.filter_by(
            job_id=job_id,
            student_id=current_user_id
        ).first()
        
        if existing_application:
            return jsonify({'error': 'Already applied to this job'}), 400
        
        data = request.get_json()
        
        # Create application
        application = Application(
            job_id=job_id,
            student_id=current_user_id,
            cover_letter=data.get('cover_letter'),
            resume_path=data.get('resume_path')
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application': application.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/my-jobs', methods=['GET'])
@jwt_required()
def get_my_jobs():
    """Get jobs posted by current alumni"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.user_type != 'alumni':
            return jsonify({'error': 'Only alumni can view their posted jobs'}), 403
        
        jobs = Job.query.filter_by(alumni_id=current_user_id).order_by(Job.created_at.desc()).all()
        
        return jsonify({
            'count': len(jobs),
            'jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/my-applications', methods=['GET'])
@jwt_required()
def get_my_applications():
    """Get applications submitted by current student"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.user_type != 'student':
            return jsonify({'error': 'Only students can view their applications'}), 403
        
        applications = Application.query.filter_by(student_id=current_user_id).order_by(Application.applied_at.desc()).all()
        
        return jsonify({
            'count': len(applications),
            'applications': [app.to_dict() for app in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<int:job_id>/applications', methods=['GET'])
@jwt_required()
def get_job_applications(job_id):
    """Get all applications for a specific job (only by alumni who posted it)"""
    try:
        current_user_id = get_jwt_identity()
        job = Job.query.get(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        if job.alumni_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        applications = Application.query.filter_by(job_id=job_id).order_by(Application.applied_at.desc()).all()
        
        return jsonify({
            'count': len(applications),
            'applications': [app.to_dict() for app in applications]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(application_id):
    """Update application status (only by alumni who posted the job)"""
    try:
        current_user_id = get_jwt_identity()
        application = Application.query.get(application_id)
        
        if not application:
            return jsonify({'error': 'Application not found'}), 404
        
        if application.job.alumni_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        application.status = data['status']
        db.session.commit()
        
        return jsonify({
            'message': 'Application status updated',
            'application': application.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
