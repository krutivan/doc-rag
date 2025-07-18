from abc import ABC, abstractmethod

class BaseEmbeddingModel(ABC):
    @abstractmethod
    def get_embeddings(self, documents: list[str]) -> list[list[float]]:
        """Return a list of embeddings for a list of documents."""
        pass
