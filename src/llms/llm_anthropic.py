from langchain_community.chat_models import ChatAnthropic
from src.llms.llm_base import LLMBase

class LLMAnthropic(LLMBase):
    def __init__(self, model_name: str, api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key
        self.llm = ChatAnthropic(model=model_name, anthropic_api_key=api_key)

    def query(self, messages, prompt: str):
        return self.llm.invoke(messages + [prompt])
