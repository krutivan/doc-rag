import uuid
from collections import defaultdict

from langchain_core.messages import HumanMessage

from src.core.dto.chat_dto import ChatMessageResponse
from src.agents.chat_agent import ChatAgent
from src.agents.chat_agent_state import AgentState
from src.core.config.config_reader import app_config

from src.services.chat.base_chat_service import BaseChatService

class InMemoryChatService(BaseChatService):
    def __init__(self):
        self.chats = defaultdict(list)
        self.max_history = self.get_max_history()

    def create_new_chat(self) -> str:
        """
        Creates a new chat session and returns the chat_id string.
        """
        chat_id = str(uuid.uuid4())
        self.chats[chat_id] = []
        return chat_id

    def chat_message(self, chat_id: str, user_prompt: str) -> ChatMessageResponse:
        """
        Accepts a chat_id and user prompt, returns a ChatMessageResponse DTO.
        For now, returns empty content.
        """
        agent = ChatAgent()
        self.chats[chat_id].append(HumanMessage(content=user_prompt))
        chat_state_history = self.chats[chat_id]
        # Only keep the last max_history messages
        if len(self.chats[chat_id]) > self.max_history:
            chat_state_history = self.chats[chat_id][-self.max_history:]
        
        # Invoke chat agent with chat history
        initial_state = AgentState(messages=chat_state_history)
        updated_state = agent.graph.invoke(initial_state)

        # Update chat history
        self.chats[chat_id] = updated_state['messages']
        return ChatMessageResponse(
            response_message=updated_state['messages'][-1].content,
            follow_up_questions=updated_state['follow_up_questions']
        )

    def get_max_history(self) -> int:
        return app_config.chat.max_history

    def get_chat_history(self, chat_id: str):
        """
        Returns the chat history for a given chat id.
        """
        return self.chats.get(chat_id, [])

# Create a singleton instance
chat_service = InMemoryChatService()
