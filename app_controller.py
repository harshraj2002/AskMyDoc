from document_processor import DocumentProcessor
from vector_store import VectorStoreManager
from llm_manager import LLMManager
import os
import json
import re
from datetime import datetime

class AskMyDocController:
    def __init__(self):
        #Optimized for speed
        self.doc_processor = DocumentProcessor(chunk_size=300, chunk_overlap=30)
        self.vector_manager = VectorStoreManager()
        self.llm_manager = LLMManager()
        self.current_qa_chain = None
        self.document_metadata = {}
    
    def _sanitize_collection_name(self, name: str) -> str:
        name = os.path.splitext(name)[0]
        name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)[:30]  
        if len(name) < 3:
            name = f"doc_{name}"
        if not name[0].isalpha():
            name = f"doc_{name}"
        return name
    
    def process_new_document_with_progress(self, uploaded_file, progress_callback=None):
        try:
            if progress_callback:
                progress_callback("Processing document...", 20)
            
            chunks = self.doc_processor.process_uploaded_file(uploaded_file)
            
            #Limit chunks for faster processing
            if len(chunks) > 20:
                chunks = chunks[:20]  
                print(f"Limited to first 20 chunks for speed")
            
            if progress_callback:
                progress_callback(f"Created {len(chunks)} chunks", 40)
            
            doc_id = uploaded_file.name
            sanitized_id = self._sanitize_collection_name(doc_id)
            collection_name = f"doc_{sanitized_id}"
            
            if progress_callback:
                progress_callback("Creating embeddings...", 60)
            
            #Fast vector store creation
            self.vector_manager.collection_name = collection_name
            vectorstore = self.vector_manager.create_vectorstore(chunks)
            
            if progress_callback:
                progress_callback("Setting up Q&A...", 80)
            
            self.current_qa_chain = self.llm_manager.create_qa_chain(vectorstore)
            
            #Save metadata
            self.document_metadata = {
                "doc_id": sanitized_id,
                "original_filename": uploaded_file.name,
                "chunks_count": len(chunks),
                "chunk_size": self.doc_processor.chunk_size,
                "chunk_overlap": self.doc_processor.chunk_overlap,
                "processed_at": str(datetime.now())
            }
            
            #Create documents directory and save metadata
            os.makedirs("./documents", exist_ok=True)
            with open(f"./documents/{sanitized_id}_metadata.json", 'w') as f:
                json.dump(self.document_metadata, f, indent=2)
            
            if progress_callback:
                progress_callback("Complete!", 100)
            
            return {
                "success": True,
                "message": f"Fast processing: {len(chunks)} chunks created",
                "doc_id": sanitized_id,
                "original_name": uploaded_file.name
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_new_document(self, uploaded_file, doc_name: str = None):
        return self.process_new_document_with_progress(uploaded_file)
    
    def ask_question(self, question: str) -> dict:
        if not self.current_qa_chain:
            return {"answer": "Please upload a document first.", "success": False}
        
        return self.llm_manager.answer_question(self.current_qa_chain, question)
    
    def load_saved_document(self, doc_id: str):
        try:
            sanitized_id = self._sanitize_collection_name(doc_id)
            collection_name = f"doc_{sanitized_id}"
            
            self.vector_manager.collection_name = collection_name
            vectorstore = self.vector_manager.load_vectorstore()
            self.current_qa_chain = self.llm_manager.create_qa_chain(vectorstore)
            
            #Load metadata
            metadata_path = f"./documents/{sanitized_id}_metadata.json"
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self.document_metadata = json.load(f)
            
            return {"success": True, "message": "Document loaded successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_current_document_info(self) -> dict:
        """Get information about currently loaded document"""
        return self.document_metadata
    
    def clear_current_document(self):
        """Clear current document and free memory"""
        self.current_qa_chain = None
        self.document_metadata = {}
        self.vector_manager.vectorstore = None