
import uuid


class ChatService:
    def create_new_chat(self) -> str:
        """
        Creates a new chat session and returns a unique UUID for it.
        
        Returns:
            str: UUID for the new chat session
        """
        return str(uuid.uuid4())

# Create a singleton instance
chat_service = ChatService()
