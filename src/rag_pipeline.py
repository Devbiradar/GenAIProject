import os
import google.generativeai as genai
from dotenv import load_dotenv
from vector_db import VectorDB
from embedding_engine import EmbeddingEngine

load_dotenv()

class RAGPipeline:
    def __init__(self, vector_db=None, embedding_engine=None):
        """
        Initializes the RAG pipeline.
        """
        self.vector_db = vector_db if vector_db else VectorDB()
        self.embedding_engine = embedding_engine if embedding_engine else EmbeddingEngine()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key.strip())
            self.model = genai.GenerativeModel('gemini-flash-latest')

    def retrieve_relevant_careers(self, query_text, n_results=3):
        """
        Retrieves relevant career paths from the Vector DB.
        """
        # Generate embedding for the query
        query_embedding = self.embedding_engine.generate_embedding(query_text)
        
        # Query the database
        results = self.vector_db.query_by_embedding(query_embedding, n_results=n_results)
        return results

    def generate_response(self, context, query):
        """
        Generates a response using Gemini based on the retrieved context.
        """
        if not hasattr(self, 'model'):
            return "Error: Gemini model not initialized. Check API Key."

        prompt = f"""
        You are a career counselor AI. Use the following context to answer the user's question about career paths.
        
        Context:
        {context}
        
        User Question:
        {query}
        
        Answer:
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

if __name__ == "__main__":
    # Test the pipeline
    rag = RAGPipeline()
    # Assuming DB is populated
    query = "I know Python and want to be a Data Scientist."
    results = rag.retrieve_relevant_careers(query)
    print("Retrieved:", results)
    
    # Simple generation test (requires API key)
    context = str(results)
    answer = rag.generate_response(context, query)
    print("Answer:", answer)
