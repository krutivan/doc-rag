
from flask import Blueprint, jsonify
import sys
import os

# Add the services directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'services'))

from chat.chat_service import chat_service

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/new', methods=['POST'])
def create_new_chat():
    """
    Creates a new chat session and returns the UUID.
    
    Returns:
        JSON response with the new chat UUID
    """
    try:
        chat_id = chat_service.create_new_chat()
        return jsonify({
            "chat_id": chat_id,
            "status": "success",
            "message": "New chat created successfully"
        }), 201
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to create new chat: {str(e)}"
        }), 500
