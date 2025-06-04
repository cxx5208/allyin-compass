import json
import os
from sentence_transformers import SentenceTransformer
import chromadb

# Configuration
JSONL_PATH = 'data/unstructured/parsed.jsonl'
COLLECTION_NAME = 'allyin_compass_documents'
# Using a small, fast model for demonstration. Consider larger models for better accuracy.
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

def load_documents(jsonl_path):
    """Loads documents from a JSONL file."""
    documents = []
    if not os.path.exists(jsonl_path):
        print(f"Error: File not found at {jsonl_path}")
        return documents
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                documents.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON line: {line.strip()} - {e}")
    print(f"Loaded {len(documents)} documents from {jsonl_path}")
    return documents

def generate_embeddings(documents, model_name):
    """Generates embeddings for the text in documents."""
    model = SentenceTransformer(model_name)
    # Extract text from documents, handling potential None values
    texts = [doc.get('text', '') for doc in documents]
    print(f"Generating embeddings for {len(texts)} texts using model {model_name}...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist() # Convert to list for ChromaDB
    print("Embedding generation complete.")
    return embeddings

def upload_embeddings_to_chromadb(client, collection_name, documents, embeddings):
    """Uploads document embeddings and payload to ChromaDB."""
    # Get or create collection
    try:
        collection = client.create_collection(name=collection_name)
        print(f"Collection '{collection_name}' created.")
    except: # Assuming collection already exists if creation fails
        collection = client.get_collection(name=collection_name)
        print(f"Collection '{collection_name}' already exists.")

    ids = []
    metadatas = []
    documents_to_add = [] # ChromaDB calls the text content 'documents'

    for i, doc in enumerate(documents):
        ids.append(str(i)) # ChromaDB requires string IDs
        # Create metadata from document metadata, excluding the large text field
        metadata = {
            'filepath': doc.get('filepath'),
            'filename': doc.get('filename'),
            'subject': doc.get('subject'),
            # Optionally store a snippet of text instead of the whole text
            'text_snippet': doc.get('text', '')[:500] + '...' if doc.get('text') else None
        }
        metadatas.append(metadata)
        # Use the original text content for ChromaDB's 'documents' field
        documents_to_add.append(doc.get('text', ''))

    if not ids:
        print("No documents to add to ChromaDB.")
        return

    print(f"Adding {len(ids)} documents to ChromaDB collection '{collection_name}'...")
    collection.add(
        embeddings=embeddings,
        documents=documents_to_add,
        metadatas=metadatas,
        ids=ids
    )
    print("Upload complete.")
    print(f"Current count in collection '{collection_name}': {collection.count()}")

if __name__ == "__main__":
    # 1. Load documents
    documents = load_documents(JSONL_PATH)

    if not documents:
        print("No documents loaded. Skipping embedding and upload.")
    else:
        # 2. Generate embeddings
        embeddings = generate_embeddings(documents, EMBEDDING_MODEL)

        # 3. Initialize ChromaDB client
        # ChromaDB will store data in a local directory './chroma_db'
        client = chromadb.PersistentClient(path="./chroma_db")

        # 4. Upload embeddings to ChromaDB
        upload_embeddings_to_chromadb(client, COLLECTION_NAME, documents, embeddings) 