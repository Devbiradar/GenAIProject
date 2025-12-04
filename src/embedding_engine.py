import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingEngine:
    def __init__(self, model_name='models/text-embedding-004'):
        """
        Initializes the embedding model using Gemini.
        """
        print(f"Loading embedding model: {model_name}...")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key.strip())
        self.model_name = model_name
        print("Model loaded successfully.")

    def generate_embedding(self, text):
        """
        Generates an embedding for the given text.
        Returns a list of floats.
        """
        if not text or not isinstance(text, str):
            raise ValueError("Input text must be a non-empty string.")
        
        result = genai.embed_content(
            model=self.model_name,
            content=text,
            task_type="retrieval_document",
            title="Embedding of text"
        )
        return result['embedding']

    def generate_embeddings_batch(self, texts):
        """
        Generates embeddings for a list of texts.
        """
        if not texts or not isinstance(texts, list):
            raise ValueError("Input must be a list of strings.")
            
        # Gemini batch embedding might have limits, doing loop for safety or check API
        # For now, simple loop
        embeddings = []
        for text in texts:
            embeddings.append(self.generate_embedding(text))
        return embeddings

if __name__ == "__main__":
    # Test the engine
    engine = EmbeddingEngine()
    sample_text = "Software Engineer with Python experience."
    try:
        emb = engine.generate_embedding(sample_text)
        print(f"Generated embedding of length: {len(emb)}")
        print(f"Sample values: {emb[:5]}")
    except Exception as e:
        print(f"Error: {e}")
