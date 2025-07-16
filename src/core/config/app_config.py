from token import OP
from pydantic import BaseModel, Field
from typing import Dict, Optional
from src.core.constants.model_type import ModelType

class AppInfoConfig(BaseModel):
    name: str
    version: str
    description: Optional[str] = None

class LLMConfig(BaseModel):
    type: ModelType
    model_name: str
    api_key: str

class ChatConfig(BaseModel):
    selected_llm: Optional[LLMConfig] = None
    max_history: int

class FastAPISettings(BaseModel):
    host: str = Field(default="0.0.0.0", description="Host for FastAPI server")
    port: int = Field(default=8000, description="Port for FastAPI server")
    api_prefix: str = Field(default="/api/v1", description="API prefix for routes")

class AppConfig(BaseModel):
    app: AppInfoConfig
    chat: ChatConfig
    llm: Dict[str, LLMConfig]
    api_settings: FastAPISettings