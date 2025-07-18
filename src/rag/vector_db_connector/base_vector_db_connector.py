from abc import ABC, abstractmethod
from typing import Any

class BaseVectorDBConnector(ABC):
    @abstractmethod
    def add_chunks(self, chunks: list[str], embeddings: list[list[float]], metadatas: list[dict], **kwargs):
        """Add chunks to the vector DB with metadata for each chunk."""
        pass

    @abstractmethod
    def query(self, query: str, n_results: int = 5, **kwargs):
        """Query the vector DB for similar documents."""
        pass
