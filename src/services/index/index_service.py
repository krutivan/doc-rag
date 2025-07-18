import os
from src.rag.indexer.indexer_factory import IndexerFactory
import os

class IndexService:
    @staticmethod
    def index(file_path: str) -> int:
        """
        Uses IndexerFactory to get the appropriate indexer (document or code) based on file extension,
        indexes the file, and returns the number of chunks.
        """
        ext = os.path.splitext(file_path)[1].lower()
        indexer = IndexerFactory.get_indexer(ext)
        # Assuming index_document returns a list of chunks or the number of chunks
        chunks = indexer.index_document(file_path)
        # If index_document returns the actual chunks
        if isinstance(chunks, list):
            return len(chunks)
        # If index_document returns just the number
        elif isinstance(chunks, int):
            return chunks
        else:
            raise ValueError("index_document() must return a list or int representing the number of chunks.")
