from src.core.constants.embedding_model_type import EmbeddingModelType
from .sentence_embedding_model import SentenceEmbeddingModel

class EmbeddingModelFactory:
    @staticmethod
    def create(model_type: EmbeddingModelType, model_name: str = None):
        if model_type == EmbeddingModelType.ALL_MINILM_L6_V2.value:
            return SentenceEmbeddingModel(model_name or "all-MiniLM-L6-v2")
        else:
            raise ValueError(f"Unsupported embedding model type: {model_type}")
