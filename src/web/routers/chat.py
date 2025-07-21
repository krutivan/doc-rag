
from fastapi import APIRouter, status
from src.services.chat.chat_service import chat_service
from src.core.dto.chat_dto import ChatCreateResponse, ChatMessageResponse
import logging
from fastapi import Body

router = APIRouter()

@router.post('/chat/new', status_code=status.HTTP_201_CREATED, response_model=ChatCreateResponse)
def create_new_chat():
    """
    Creates a new chat session and returns the UUID.
    """
    try:
        chat_id = chat_service.create_new_chat()
        return ChatCreateResponse(chat_id=chat_id)
    except Exception as e:
        return ChatCreateResponse(
            chat_id="",
            status="error",
            message=f"Failed to create new chat: {str(e)}"
        )

@router.post('/chat/message', response_model=ChatMessageResponse)
def chat_message(chat_id: str = Body(...), user_message: str = Body(...)):
    """
    Accepts a chat id and user message, returns a chat message response.
    """
    try:
        return chat_service.chat_message(chat_id, user_message)
    except Exception as e:
        logging.error(f"Failed to process chat message: {str(e)}")
        return ChatMessageResponse(
            response_message="",
            follow_up_questions=""
        )

@router.post('/chat/history')
def chat_history(chat_id: str = Body(...)):
    """
    Returns the chat history for a given chat id.
    """
    try:
        return chat_service.get_chat_history(chat_id)
    except Exception as e:
        logging.error(f"Failed to get chat history: {str(e)}")
        return {"error": str(e)}
