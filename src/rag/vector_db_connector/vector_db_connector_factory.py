from src.core.constants.vector_db_type import VectorDBType

from .chromadb_connector import ChromaDBConnector
from .pinecone_connector import PineconeConnector
from .base_vector_db_connector import BaseVectorDBConnector

class VectorDBConnectorFactory:
    @staticmethod
    def create(db_name: str, db_config, persist_dir: str = None) -> BaseVectorDBConnector:
        db_type = getattr(db_config, 'type', None)
        if db_type == VectorDBType.CHROMADB:
            return ChromaDBConnector(db_config, persist_dir)
        elif db_type == VectorDBType.PINECONE:
            return PineconeConnector(db_config)
        else:
            raise ValueError(f"Unsupported vector DB type: {db_type}")
