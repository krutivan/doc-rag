from pydantic import BaseModel

class ChatCreateResponse(BaseModel):
    chat_id: str
    status: str = "success"
    message: str = "New chat created successfully"

class ChatMessageResponse(BaseModel):
    response_message: str
