from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from typing import List
import chromadb

class VectorStoreManager:
    def __init__(self, collection_name="askmydoc", persist_directory="./chroma_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        #Initialize Nomic embeddings via Ollama
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434"
        )
        
        #Initialize ChromaDB
        self.vectorstore = None
    
    def create_vectorstore(self, documents: List[Document]):
        """Create vector store from documents"""
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory
        )
        self.vectorstore.persist()
        return self.vectorstore
    
    def load_vectorstore(self):
        """Load existing vector store"""
        self.vectorstore = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        return self.vectorstore
    
    def similarity_search(self, query: str, k: int = 6):
        """Search for similar documents with increased k for more context"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        return self.vectorstore.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = 6):
        """Search with relevance scores"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        return self.vectorstore.similarity_search_with_score(query, k=k)
    
    def add_documents(self, documents: List[Document]):
        """Add new documents to existing vector store"""
        if not self.vectorstore:
            self.create_vectorstore(documents)
        else:
            self.vectorstore.add_documents(documents)
            self.vectorstore.persist()