from vector_db import VectorDB
from embedding_engine import EmbeddingEngine

def ingest_dummy_data():
    """
    Ingests dummy career data into the Vector DB.
    """
    db = VectorDB()
    engine = EmbeddingEngine()
    
    careers = [
        {
            "role": "Data Scientist",
            "description": "Analyze large datasets to derive insights. Requires Python, SQL, Machine Learning, and Statistics.",
            "category": "Data"
        },
        {
            "role": "Frontend Developer",
            "description": "Build user interfaces for web applications. Requires HTML, CSS, JavaScript, React, and responsive design.",
            "category": "Web Development"
        },
        {
            "role": "Backend Developer",
            "description": "Build server-side logic and APIs. Requires Python (Django/Flask), Node.js, Databases (SQL/NoSQL).",
            "category": "Web Development"
        },
        {
            "role": "DevOps Engineer",
            "description": "Manage infrastructure and deployment pipelines. Requires Docker, Kubernetes, CI/CD, and Cloud platforms (AWS/Azure).",
            "category": "Infrastructure"
        },
        {
            "role": "Product Manager",
            "description": "Define product vision and strategy. Requires communication, prioritization, and understanding of user needs.",
            "category": "Management"
        }
    ]
    
    documents = [c["description"] for c in careers]
    metadatas = [{"role": c["role"], "category": c["category"]} for c in careers]
    ids = [str(i) for i in range(len(careers))]
    
    print("Generating embeddings...")
    embeddings = engine.generate_embeddings_batch(documents)
    
    print("Adding to Vector DB...")
    db.add_documents_with_embeddings(documents, embeddings, metadatas, ids)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_dummy_data()
