from abc import ABC, abstractmethod

class BaseIndexer(ABC):
    @abstractmethod
    def index_document(self, file_path: str):
        """Indexes a document given its file path."""
        pass
