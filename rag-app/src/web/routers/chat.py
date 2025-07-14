
from fastapi import APIRouter, status
from services.chat.chat_service import chat_service

router = APIRouter()

@router.post('/chat/new', status_code=status.HTTP_201_CREATED)
def create_new_chat():
    """
    Creates a new chat session and returns the UUID.
    """
    try:
        chat_id = chat_service.create_new_chat()
        return {
            "chat_id": chat_id,
            "status": "success",
            "message": "New chat created successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create new chat: {str(e)}"
        }
