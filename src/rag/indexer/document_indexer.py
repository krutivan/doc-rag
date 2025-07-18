import os
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.rag.embedding_model.embedding_model_factory import EmbeddingModelFactory
from src.rag.vector_db_connector.vector_db_connector_factory import VectorDBConnectorFactory
from src.core.config.config_reader import app_config
from src.rag.indexer.base_indexer import BaseIndexer
from src.core.utils.file_utils import FileUtils

class DocumentIndexer(BaseIndexer):
    def __init__(self):
        # Get vector DB config and persist dir from app config
        self.vector_db_config = app_config.index.vector_db
        self.persist_dir = app_config.app.data_path
        self.vector_db = VectorDBConnectorFactory.create(
            db_name=app_config.index.vector_db.type.value,
            db_config=self.vector_db_config,
            persist_dir=self.persist_dir
        )
        self.embedding_model = EmbeddingModelFactory.create(app_config.index.embedding_model)

    def index_document(self, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        chunks = []
        # Use langchain document loaders based on extension
        if ext in ['.txt', '.md']:
            chunks = self._load_and_chunk_text_file(file_path)
        elif ext in ['.pdf']:
            chunks = self._load_and_chunk_pdf_file(file_path)
        else:
            raise ValueError("Unsupported file extension")
        
        # add chunk to configured vector db
        self._add_chunks_to_vector_db(chunks)
        return len(chunks)

    def _load_and_chunk_text_file(self, file_path: str):
        from langchain_community.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        loader = TextLoader(file_path)
        documents = loader.load()
        return self._recursive_text_splitter(documents)
        
    def _load_and_chunk_pdf_file(self, file_path: str):
        from langchain_community.document_loaders import PyPDFLoader
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return self._recursive_text_splitter(documents)
    
    def _recursive_text_splitter(self, documents: list[Document]):
        # TODO: Make splitter/chunker config driven
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return text_splitter.split_documents(documents)
    
    def _add_chunks_to_vector_db(self, chunks: list[Document]):
        texts = [doc.page_content for doc in chunks]
        embeddings = self.embedding_model.get_embeddings(texts)
        metadatas = [{"filename": FileUtils.get_filename(chunks[0].metadata['source'])} for _ in texts]
        self.vector_db.add_chunks(texts, embeddings, metadatas)