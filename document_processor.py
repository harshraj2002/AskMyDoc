from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Fixed import
from langchain.schema import Document
import os
from typing import List

class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        #Use more sophisticated text splitter for better context preservation
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", ";", ":", " ", ""],
            keep_separator=True,
            length_function=len,
            is_separator_regex=False
        )
    
    def validate_file_size(self, file_size, max_size_mb=10):
        """Validate file size to prevent slow processing"""
        if file_size > max_size_mb * 1024 * 1024:
            return False, f"File too large. Maximum size: {max_size_mb}MB"
        return True, "File size OK"
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load document based on file extension"""
        _, ext = os.path.splitext(file_path.lower())
        
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext == '.docx':
            loader = Docx2txtLoader(file_path)
        elif ext == '.txt':
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
        documents = loader.load()
        
        #Split documents with metadata preservation
        chunks = self.text_splitter.split_documents(documents)
        
        #Add chunk index to metadata for better tracking
        for i, chunk in enumerate(chunks):
            chunk.metadata['chunk_index'] = i
            chunk.metadata['chunk_size'] = len(chunk.page_content)
        
        return chunks
    
    def process_uploaded_file(self, uploaded_file) -> List[Document]:
        """Process file uploaded through web interface"""
        #Validate file size
        is_valid, message = self.validate_file_size(uploaded_file.size)
        if not is_valid:
            raise ValueError(message)
        
        #Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            chunks = self.load_document(temp_path)
            return chunks
        finally:
            #Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)