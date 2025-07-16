import os
import yaml
from core.config.app_config import (
    AppConfig, AppInfoConfig, ChatConfig, LLMConfig, FastAPISettings
)
from src.core.constants.model_type import ModelType

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.yaml')

def _read_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

_config = _read_config()

# Parse app section
app_section = _config.get('app', {})
app_info = AppInfoConfig(
    name=app_section.get('name', ''),
    version=app_section.get('version', ''),
    description=app_section.get('description')
)

# Parse llm section
llm_section = _config.get('llm', {})
llm_configs = {}
for llm_name, llm_conf in llm_section.items():
    llm_configs[llm_name] = LLMConfig(
        type=ModelType(llm_conf.get('type')),
        model_name=llm_conf.get('model_name', ''),
        api_key=llm_conf.get('api_key', '')
    )

# Parse chat section
chat_section = _config.get('chat', {})
chat_config = ChatConfig(
    selected_llm=None,
    max_history=int(chat_section.get('max_history', 5))
)

# Attach selected_llm config to chat_config
selected_llm_name = getattr(chat_config, 'selected_llm', None)
if selected_llm_name and selected_llm_name in llm_configs:
    chat_config.selected_llm = llm_configs[selected_llm_name]
else:
    raise ValueError(f"Config error: selected chat LLM '{selected_llm_name}' not found in llm configs: {list(llm_configs.keys())}")


# Parse FastAPI server settings
fast_api_server = _config.get('fast_api_server', {})
fastapi_settings = FastAPISettings(
    host=fast_api_server.get('host', '0.0.0.0'),
    port=int(fast_api_server.get('port', 8000)),
    api_prefix=fast_api_server.get('api', {}).get('prefix', '/api/v1')
)

app_config = AppConfig(
    app=app_info,
    chat=chat_config,
    llm=llm_configs,
    api_settings=fastapi_settings
)
