# AskMyDoc

- An intelligent Document Q&A Assistant.
- Built with LangChain, Ollama (Llama 3.2), and Nomic Embeddings. Upload documents and ask questions to get accurate, contextual answers based on the document content.

## Features

- **Multi-format Support**: Upload PDF, DOCX, and TXT files
- **Intelligent Q&A**: Get accurate answers based strictly on document content
- **Fast Processing**: Optimized for speed with smart chunking and batching
- **Real-time Progress**: Visual feedback during document processing
- **Document Management**: Save and reload processed documents
- **Source Transparency**: View which parts of the document were used to generate answers
- **Local Processing**: Complete privacy - all processing happens locally

## Tech Stack

- **LangChain**: Document processing and chain orchestration
- **Ollama**: Local LLM hosting (Llama 3.2)
- **Nomic Embeddings**: Document vectorization
- **ChromaDB**: Vector database for document storage
- **Streamlit**: Web interface
- **Python**: Backend processing

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running
- 4GB+ RAM recommended

## Installation

### 1. Clone the Repository
```
git clone <repository-url>
cd askmydoc
```

### 2. Create Virtual Environment
```
# Windows
python -m venv askmydoc-env
askmydoc-env\Scripts\activate

# Linux/macOS
python -m venv askmydoc-env
source askmydoc-env/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Install and Setup Ollama
```
# Download and install Ollama from https://ollama.ai
# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text
```

## Usage

### 1. Start Ollama Service
```
ollama serve
```
Keep this terminal open - Ollama needs to run in the background.

### 2. Start AskMyDoc
```
streamlit run streamlit_app.py
```

### 3. Access the Application
Open your browser and go to `http://localhost:8501`

### 4. Upload and Process Documents
- Click "Choose a file" in the sidebar
- Select a PDF, DOCX, or TXT file (max 5MB for optimal speed)
- Click "Process Document"
- Wait for processing to complete

### 5. Ask Questions
- Type questions in the chat interface
- Get answers based on your document content
- View source context to verify information

## File Structure

```
askmydoc/
├── document_processor.py    # Document loading and chunking
├── vector_store.py         # Vector database management
├── llm_manager.py          # LLM and chain management
├── app_controller.py       # Main application controller
├── streamlit_app.py        # Web interface
├── requirements.txt        # Python dependencies
├── askmydoc-env/          # Virtual environment
├── chroma_db/             # Vector database storage
└── documents/             # Document metadata storage
```

## Configuration

### Performance Optimization
The system is optimized for speed with these default settings:
- **Chunk Size**: 300 characters
- **Chunk Overlap**: 30 characters
- **Max Chunks**: 20 per document
- **Retrieval Count**: 2 documents per query
- **Context Window**: 2048 tokens

### Customization
You can modify these settings in the respective files:
- Document processing: `document_processor.py`
- Vector storage: `vector_store.py`
- LLM settings: `llm_manager.py`

## Usage Tips

### For Best Results:
- Use clear, specific questions
- Keep documents under 5MB for fast processing
- Text files process fastest, followed by DOCX, then PDF
- Ask one question at a time for accuracy

### Example Questions:
- "What is the main topic of this document?"
- "What are the key points mentioned about [topic]?"
- "Summarize the main findings"
- "What does the document say about [specific term]?"

### Document Management:
- Processed documents are saved automatically
- Use the Document ID to reload previously processed documents
- Clear current document to free memory when switching

## Troubleshooting

### Common Issues:

**"No module named" errors:**
```
pip install --upgrade langchain langchain-community langchain-ollama langchain-text-splitters
```

**Ollama connection errors:**
```
# Check if Ollama is running
ollama list
curl http://localhost:11434/api/tags

# Restart if needed
ollama serve
```

**Slow processing:**
- Use smaller documents (under 5MB)
- Close other applications to free memory
- Use text files when possible

**No answers from document:**
- Ensure document uploaded successfully
- Check that questions are related to document content
- Try rephrasing questions more specifically

### Debug Mode:
For troubleshooting, check the terminal where you ran `streamlit run` for detailed error messages.

## Performance

### Expected Processing Times:
- **Small documents (1-3 pages)**: 15-30 seconds
- **Medium documents (5-10 pages)**: 30-60 seconds
- **Large documents**: Limited to first 20 chunks for consistent speed

### Hardware Requirements:
- **Minimum**: 4GB RAM, 2GB free disk space
- **Recommended**: 8GB+ RAM for better performance
- **Storage**: ~1GB for models, plus document storage

## Limitations

- Maximum file size: 5MB (configurable)
- Large documents processed in chunks (first 20 chunks for speed)
- Requires internet connection for initial model download
- Local processing only - no cloud features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review error messages in the terminal
3. Ensure all prerequisites are properly installed
4. Create an issue in the repository

## Changelog

### v1.0.0
- Initial release with basic Q&A functionality
- Support for PDF, DOCX, and TXT files
- Local processing with Ollama and LangChain

### v1.1.0 (Current)
- Speed optimizations for faster document processing
- Improved error handling and user feedback
- Better document management features
- Enhanced UI with progress tracking

## Acknowledgments

- LangChain team for the excellent framework
- Ollama team for local LLM hosting
- Nomic team for embedding models
- Streamlit team for the web interface framework

---

**Built with ❤️ using LangChain, Ollama, and Streamlit**

```

