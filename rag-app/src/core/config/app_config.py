
from pydantic import BaseModel, Field

class DatabaseConfig(BaseModel):
    pass

class FastAPISettings(BaseModel):
    host: str = Field(default="0.0.0.0", description="Host for FastAPI server")
    port: int = Field(default=8000, description="Port for FastAPI server")
    api_prefix: str = Field(default="/api/v1", description="API prefix for routes")

class AppConfig(BaseModel):
    database: DatabaseConfig
    api_settings: FastAPISettings