from src.core.constants.embedding_model_type import EmbeddingModelType
from .base_embedding_model import BaseEmbeddingModel

class SentenceEmbeddingModel(BaseEmbeddingModel):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model_type = EmbeddingModelType.ALL_MINILM_L6_V2
        self.model_name = model_name
        self.embedder = SentenceTransformer(model_name)

    def get_embeddings(self, documents: list[str]) -> list[list[float]]:
        embeddings = self.embedder.encode(documents)
        return embeddings.tolist()
