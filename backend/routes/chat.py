from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Message, Conversation, User
from sqlalchemy import or_, and_

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    """Get all conversations for the current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get all conversations where user is participant
        conversations = Conversation.query.filter(
            or_(
                Conversation.user1_id == current_user_id,
                Conversation.user2_id == current_user_id
            )
        ).order_by(Conversation.last_message_at.desc()).all()
        
        conversation_list = []
        for conv in conversations:
            # Determine the other user
            other_user = conv.user2 if conv.user1_id == current_user_id else conv.user1
            
            # Get last message
            last_message = Message.query.filter(
                or_(
                    and_(Message.sender_id == conv.user1_id, Message.receiver_id == conv.user2_id),
                    and_(Message.sender_id == conv.user2_id, Message.receiver_id == conv.user1_id)
                )
            ).order_by(Message.created_at.desc()).first()
            
            # Count unread messages
            unread_count = Message.query.filter_by(
                receiver_id=current_user_id,
                sender_id=other_user.id,
                is_read=False
            ).count()
            
            conversation_list.append({
                'conversation_id': conv.id,
                'other_user': other_user.to_dict(),
                'last_message': last_message.to_dict() if last_message else None,
                'unread_count': unread_count,
                'last_message_at': conv.last_message_at.isoformat() if conv.last_message_at else None
            })
        
        return jsonify({
            'count': len(conversation_list),
            'conversations': conversation_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/messages/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_messages(other_user_id):
    """Get all messages between current user and another user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if other user exists
        other_user = User.query.get(other_user_id)
        if not other_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get all messages between the two users
        messages = Message.query.filter(
            or_(
                and_(Message.sender_id == current_user_id, Message.receiver_id == other_user_id),
                and_(Message.sender_id == other_user_id, Message.receiver_id == current_user_id)
            )
        ).order_by(Message.created_at.asc()).all()
        
        # Mark received messages as read
        Message.query.filter_by(
            sender_id=other_user_id,
            receiver_id=current_user_id,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()
        
        return jsonify({
            'count': len(messages),
            'messages': [msg.to_dict() for msg in messages],
            'other_user': other_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    """Send a message to another user"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'receiver_id' not in data or 'content' not in data:
            return jsonify({'error': 'receiver_id and content are required'}), 400
        
        receiver_id = data['receiver_id']
        content = data['content']
        
        # Check if receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            return jsonify({'error': 'Receiver not found'}), 404
        
        # Create message
        message = Message(
            sender_id=current_user_id,
            receiver_id=receiver_id,
            content=content
        )
        
        db.session.add(message)
        
        # Create or update conversation
        conversation = Conversation.query.filter(
            or_(
                and_(Conversation.user1_id == current_user_id, Conversation.user2_id == receiver_id),
                and_(Conversation.user1_id == receiver_id, Conversation.user2_id == current_user_id)
            )
        ).first()
        
        if not conversation:
            conversation = Conversation(
                user1_id=current_user_id,
                user2_id=receiver_id
            )
            db.session.add(conversation)
        else:
            conversation.last_message_at = message.created_at
        
        db.session.commit()
        
        return jsonify({
            'message': 'Message sent successfully',
            'data': message.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/mark-read/<int:message_id>', methods=['PUT'])
@jwt_required()
def mark_message_read(message_id):
    """Mark a specific message as read"""
    try:
        current_user_id = get_jwt_identity()
        message = Message.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        if message.receiver_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        message.is_read = True
        db.session.commit()
        
        return jsonify({'message': 'Message marked as read'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """Get total count of unread messages for current user"""
    try:
        current_user_id = get_jwt_identity()
        
        unread_count = Message.query.filter_by(
            receiver_id=current_user_id,
            is_read=False
        ).count()
        
        return jsonify({'unread_count': unread_count}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/delete/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    """Delete a message (only by sender)"""
    try:
        current_user_id = get_jwt_identity()
        message = Message.query.get(message_id)
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        if message.sender_id != current_user_id:
            return jsonify({'error': 'Unauthorized to delete this message'}), 403
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({'message': 'Message deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
