import uvicorn
import os
import sys
sys.path.append(__file__[:__file__.rfind('web') ])

from core.config.config_reader import app_config

def run_fastapi_server():
    """Run FastAPI app with uvicorn ASGI server using config.yaml settings"""
    uvicorn.run("app:app",
                host=app_config.api_settings.host,
                port=app_config.api_settings.port,
                reload=True,
                log_level="info")

if __name__ == "__main__":
    run_fastapi_server()
