from .document_indexer import DocumentIndexer
from .code_indexer import CodeIndexer

class IndexerFactory:
    @staticmethod
    def get_indexer(file_extension: str):
        """Return the appropriate indexer based on file extension."""
        doc_exts = ['.txt', '.md', '.pdf']
        code_exts = ['.py', '.js', '.java', '.cpp', '.c', '.ts', '.go', '.rb', '.rs', '.php', '.cs']
        ext = file_extension.lower()
        if ext in doc_exts:
            return DocumentIndexer()
        elif ext in code_exts:
            return CodeIndexer()
        else:
            raise ValueError(f"Unsupported file extension for indexing: {ext}")
