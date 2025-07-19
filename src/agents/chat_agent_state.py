from typing import TypedDict, List
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: List[AnyMessage]
    documents: List[str]
    document_ids: List[str]
    distances: List[float]
    follow_up_questions: str
