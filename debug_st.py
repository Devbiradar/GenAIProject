try:
    from sentence_transformers import SentenceTransformer
    print("Import successful")
    model = SentenceTransformer('all-mpnet-base-v2')
    print("Model loaded")
except Exception as e:
    print(f"Error: {e}")
