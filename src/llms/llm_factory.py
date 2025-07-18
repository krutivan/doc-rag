from src.llms.llm_open_ai import LLMOpenAI
from src.llms.llm_anthropic import LLMAnthropic
from src.llms.llm_model_type import LLMModelType

class LLMFactory:
    @staticmethod
    def create_llm(model_type: LLMModelType, model_name: str, api_key: str = None):
        if model_type.value == LLMModelType.OPENAI.value:
            return LLMOpenAI(model_name, api_key=api_key)
        elif model_type.value == LLMModelType.ANTHROPIC.value:
            return LLMAnthropic(model_name, api_key=api_key)
        else:       
            raise ValueError(f"Could not create LLM, unknown model type: {model_type}")
