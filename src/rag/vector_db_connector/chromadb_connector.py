import uuid

import chromadb

from src.core.config.app_config import VectorDBConfig
from .base_vector_db_connector import BaseVectorDBConnector


class ChromaDBConnector(BaseVectorDBConnector):
    def __init__(self, config: VectorDBConfig, persist_dir: str):
        self.config = config
        # Example: connect to chromadb (pseudo, replace with actual chromadb code)
        if self.config.in_memory:
            self.client = chromadb.Client()
        else:
            self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name="documents")

    def add_chunks(self, chunks: list[str], embeddings: list[list[float]], metadatas: list[dict], **kwargs):
        # Add chunks and embeddings to ChromaDB (pseudo)
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=[str(uuid.uuid4()) for _ in chunks]
        )

    def query(self, query: str, n_results: int = 5, **kwargs):
        # Query ChromaDB collection for similar documents
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        # Return documents, ids, and distances
        return {
            "documents": results.get("documents", [[]])[0],
            "ids": results.get("ids", [[]])[0],
            "distances": results.get("distances", [[]])[0]
        }

