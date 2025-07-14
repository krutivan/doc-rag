
from fastapi import FastAPI
from routers.health import router as health_router
from routers.chat import router as chat_router
from core.config.config_reader import app_config

app = FastAPI()

# Include routers
app.include_router(health_router)
app.include_router(chat_router, prefix=app_config.api_settings.api_prefix)

@app.get('/')
def home():
    return {"message": "RAG App is running", "status": "ok"}
