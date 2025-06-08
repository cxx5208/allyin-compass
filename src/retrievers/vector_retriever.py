import chromadb
import streamlit as st
from sentence_transformers import SentenceTransformer

# Configuration
CHROMA_DB_PATH = './chroma_db'
COLLECTION_NAME = 'allyin_compass_documents'
EMBEDDING_MODEL = 'all-MiniLM-L6-v2' # Use the same model as embedder.py

@st.cache_resource
def get_embedding_model(model_name):
    """Caches and returns the SentenceTransformer model."""
    return SentenceTransformer(model_name)

@st.cache_resource
def get_chroma_collection(db_path, collection_name):
    """Caches and returns the ChromaDB collection."""
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name=collection_name)
    return collection

def get_vector_retriever(query, k=5, db_path=CHROMA_DB_PATH, collection_name=COLLECTION_NAME, model_name=EMBEDDING_MODEL):
    """Performs a vector similarity search against the ChromaDB collection."""
    try:
        # Get the cached embedding model and ChromaDB collection
        model = get_embedding_model(model_name)
        collection = get_chroma_collection(db_path, collection_name)

        # Generate embedding for the query
        query_embedding = model.encode(query).tolist()

        # Perform the similarity search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=['documents', 'metadatas', 'distances'] # Include content, metadata, and distance
        )

        print(f"Successfully performed vector search for query: {query}")
        # The results are nested, extract the first (and only) list of results
        if results and results.get('ids') and results['ids'][0]:
             # Reformat results for easier use, combining metadata, document, and distance
            formatted_results = []
            # Check if all required keys exist and have corresponding values
            if (results.get('ids') and len(results['ids'][0]) > 0 and
                results.get('documents') and len(results['documents'][0]) > 0 and
                results.get('metadatas') and len(results['metadatas'][0]) > 0 and
                results.get('distances') and len(results['distances'][0]) > 0):

                for i in range(len(results['ids'][0])):
                    formatted_results.append({
                        'id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i]
                    })
                return formatted_results
            else:
                print("Vector search returned empty results or missing data.")
                return []

        else:
            print("No results found for the vector search query.")
            return []

    except Exception as e:
        print(f"Error performing vector search: {e}")
        # If the collection doesn't exist, a specific error might occur, handle gracefully
        if "Collection allyin_compass_documents does not exist" in str(e):
            print("ChromaDB collection not found. Please run embedder.py first.")
        return []

# Example usage (optional - for testing)
if __name__ == "__main__":
    # Make sure you have run embedder.py first to create the collection
    sample_query = "What is in the sample document?"
    search_results = get_vector_retriever(sample_query)

    if search_results:
        print("\nVector Search Results:")
        for result in search_results:
            print(f"Distance: {result['distance']:.4f}")
            print(f"Filename: {result['metadata'].get('filename', 'N/A')}")
            print(f"Text Snippet: {result['metadata'].get('text_snippet', 'N/A')}")
            print("---")
    else:
        print("No vector search results found.") 