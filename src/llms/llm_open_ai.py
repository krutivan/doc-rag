from langchain_openai import ChatOpenAI
from src.llms.llm_base import LLMBase

class LLMOpenAI(LLMBase):
    def __init__(self, model_name: str, api_key: str = None):
        self.model_name = model_name
        self.api_key = api_key
        self.llm = ChatOpenAI(model=model_name, openai_api_key=api_key)

    def query(self, messages):
        return self.llm.invoke(messages)

