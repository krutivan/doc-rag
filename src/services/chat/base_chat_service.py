from abc import ABC, abstractmethod
from src.core.dto.chat_dto import ChatMessageResponse

class BaseChatService(ABC):
    @abstractmethod
    def create_new_chat(self) -> str:
        pass

    @abstractmethod
    def chat_message(self, chat_id: str, user_prompt: str) -> ChatMessageResponse:
        pass

    @abstractmethod
    def get_max_history(self) -> int:
        pass

    @abstractmethod
    def get_chat_history(self, chat_id: str):
        pass
