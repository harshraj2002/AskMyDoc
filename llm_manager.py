from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

class LLMManager:
    def __init__(self):
        self.llm = OllamaLLM(
            model="llama3.2",
            base_url="http://localhost:11434",
            temperature=0,
            num_predict=200
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="Context: {context}\n\nQuestion: {question}\n\nAnswer based only on the context:"
        )
    
    def create_qa_chain(self, vectorstore):
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )
        return qa_chain
    
    def answer_question(self, qa_chain, question: str) -> dict:
        try:
            result = qa_chain.invoke({"query": question})
            return {
                "answer": result["result"],
                "source_documents": result.get("source_documents", []),
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"Error: {str(e)}",
                "success": False,
                "error": str(e)
            }