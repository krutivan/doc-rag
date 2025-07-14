import os
import yaml
from core.config.app_config import FastAPISettings, DatabaseConfig, AppConfig

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml')

def _read_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

_config = _read_config()
fast_api_server = _config.get('fast_api_server', {})

fastapi_settings = FastAPISettings(
    host=fast_api_server.get('host', '0.0.0.0'),
    port=int(fast_api_server.get('port', 8000)),
    api_prefix=fast_api_server.get('api', {}).get('prefix', '/api/v1')
)

database_settings = DatabaseConfig()  # Extend this as you add DB config fields

app_config = AppConfig(
    database=database_settings,
    api_settings=fastapi_settings
)
