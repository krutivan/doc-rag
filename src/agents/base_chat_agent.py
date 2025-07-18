from abc import ABC, abstractmethod
from typing import Any

class BaseChatAgent(ABC):
    @abstractmethod
    def chat(self, state: Any) -> Any:
        """
        Abstract chat method to be implemented by concrete agents.
        """
        pass
