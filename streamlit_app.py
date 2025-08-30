import streamlit as st
from app_controller import AskMyDocController
import datetime
import time

#Page configuration
st.set_page_config(
    page_title="AskMyDoc",
    page_icon="📄",
    layout="wide"
)

#Initialize session state
if 'controller' not in st.session_state:
    st.session_state.controller = AskMyDocController()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_document' not in st.session_state:
    st.session_state.current_document = None

#Header
st.title("📄 AskMyDoc")
st.subheader("An Intelligent Document Q&A Assistant")

#Sidebar for document management
with st.sidebar:
    st.header("Document Management")
    
    #Current document info
    if st.session_state.current_document:
        st.info(f"**Current Document:** {st.session_state.current_document}")
        
        #Show document metadata
        doc_info = st.session_state.controller.get_current_document_info()
        if doc_info:
            with st.expander("Document Details"):
                st.write(f"**Chunks:** {doc_info.get('chunks_count', 'N/A')}")
                st.write(f"**Processed:** {doc_info.get('processed_at', 'N/A')}")
                st.write(f"**Doc ID:** `{doc_info.get('doc_id', 'N/A')}`")
    
    #Document upload section
    st.subheader("Upload New Document")
    
    #File size warning
    st.caption("For faster processing, keep files under 10MB")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, DOCX, or TXT files (max 10MB for optimal performance)"
    )
    
    if uploaded_file and st.button("Process Document"):
        #Show file info
        file_size_mb = uploaded_file.size / (1024 * 1024)
        st.write(f"File size: {file_size_mb:.2f} MB")
        
        #Create progress bar and status text
        progress_bar = st.progress(0)
        status_text = st.empty()
        start_time = time.time()
        
        def update_progress(message, progress):
            status_text.text(message)
            progress_bar.progress(int(progress))
        
        #Process with progress tracking
        result = st.session_state.controller.process_new_document_with_progress(
            uploaded_file, 
            progress_callback=update_progress
        )
        
        #Calculate processing time
        processing_time = time.time() - start_time
        
        if result["success"]:
            st.success(f"{result['message']} (Processed in {processing_time:.1f}s)")
            st.session_state.chat_history = []
            st.session_state.current_document = result.get("original_name", result["doc_id"])
            
            #Show document ID for future reference
            if result.get("original_name") != result["doc_id"]:
                st.info(f"**Document ID for future loading:** `{result['doc_id']}`")
        else:
            st.error(f"Error: {result['error']}")
        
        #Clean up progress indicators
        progress_bar.empty()
        status_text.empty()
    
    #Pre-saved documents section
    st.subheader("Load Saved Document")
    doc_id = st.text_input("Document ID", help="Enter the document ID from previous processing")
    if st.button("Load Document"):
        with st.spinner("Loading document..."):
            result = st.session_state.controller.load_saved_document(doc_id)
            if result["success"]:
                st.success("Document loaded successfully")
                st.session_state.chat_history = []
                st.session_state.current_document = doc_id
            else:
                st.error(f"Error: {result.get('error', 'Unknown error')}")
    
    #Clear current document
    if st.button("Clear Current Document"):
        st.session_state.controller.clear_current_document()
        st.session_state.current_document = None
        st.session_state.chat_history = []
        st.rerun()

#Performance tips in sidebar
with st.sidebar:
    with st.expander("Performance Tips"):
        st.markdown("""
        **For faster processing:**
        - Use smaller documents (< 50 pages)
        - Text files process fastest
        - PDFs with images take longer
        - Keep Ollama running in background
        - Close unused applications to free memory
        
        **Processing Times:**
        - Small docs (1-5 pages): 30-60 seconds
        - Medium docs (10-20 pages): 1-3 minutes
        - Large docs (50+ pages): 3-10 minutes
        """)

#Main chat interface
st.header("Ask Your Questions")

#Display current document status
if not st.session_state.current_document:
    st.warning("No document loaded. Please upload or load a document to start asking questions.")
else:
    st.success(f"Ready to answer questions about: **{st.session_state.current_document}**")

#Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.write(chat["answer"])
        #Show timestamp for each response
        st.caption(f"Answered at {chat['timestamp'].strftime('%H:%M:%S')}")

#Question input
if question := st.chat_input("Ask a question about your document..."):
    #Add user question to chat
    with st.chat_message("user"):
        st.write(question)
    
    #Get answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            start_time = time.time()
            result = st.session_state.controller.ask_question(question)
            response_time = time.time() - start_time
            
            if result["success"]:
                st.write(result["answer"])
                st.caption(f"Response generated in {response_time:.1f}s")
                
                #Show source documents if available
                if "source_documents" in result and result["source_documents"]:
                    with st.expander("View Source Context"):
                        for i, doc in enumerate(result["source_documents"]):
                            st.write(f"**Source {i+1}:**")
                            st.write(doc.page_content[:500] + "...")
            else:
                st.error("Sorry, I encountered an error processing your question.")
    
    #Add to chat history
    st.session_state.chat_history.append({
        "question": question,
        "answer": result.get("answer", "Error occurred"),
        "timestamp": datetime.datetime.now()
    })

#Instructions
with st.expander("How to Use AskMyDoc"):
    st.markdown("""
    1. **Upload a Document**: Use the sidebar to upload PDF, DOCX, or TXT files
    2. **Process**: Click "Process Document" to analyze and index your document
    3. **Note the Document ID**: After processing, save the Document ID for future loading
    4. **Ask Questions**: Type your questions in the chat box below
    5. **Get Answers**: Receive accurate answers based strictly on your document content
    6. **Save/Load**: Use the Document ID to reload processed documents later
    
    **Performance Note**: Document names are automatically sanitized to meet database requirements. 
    Special characters and spaces are replaced with underscores for optimal processing.
    """)

#Footer
st.markdown("---")