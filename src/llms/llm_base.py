from abc import ABC
from typing import List
from langchain_core.messages import BaseMessage

class LLMBase(ABC):
    def query(
        self, 
        messages: list,
        prompt: str,
    ) -> str:
        raise NotImplementedError
