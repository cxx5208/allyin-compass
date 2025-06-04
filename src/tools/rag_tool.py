import sys
import os

# Add the parent directory of src to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from transformers import T5ForConditionalGeneration, T5Tokenizer
from src.retrievers import vector_retriever

# Configuration
# Using a small T5 model for quick demonstration
LLM_MODEL_NAME = 'google/flan-t5-small'

def initialize_llm_and_tokenizer(model_name):
    """Initializes and returns the LLM model and tokenizer."""
    print(f"Loading LLM model: {model_name}...")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    print("LLM model loaded.")
    return tokenizer, model

def build_rag_prompt(query, retrieved_documents):
    """Builds a prompt for the LLM using the query and retrieved documents."""
    context = ""
    citations = []
    if retrieved_documents:
        context += "Context:\n"
        for i, doc in enumerate(retrieved_documents):
            # Use a formatted string to clearly separate documents and add a reference number
            context += f"[Document {i+1}]\n"
            # Add text snippet or full document text if available
            if doc.get('document'):
                 context += doc['document'] + "\n"
            elif doc.get('metadata', {}).get('text_snippet'):
                 context += doc['metadata']['text_snippet'] + "\n"
            else:
                 context += "[No text content available]\n"
            # Add citation information
            if doc.get('metadata', {}).get('filename'):
                citations.append(f"[Document {i+1}] {doc['metadata']['filename']}")
            else:
                 citations.append(f"[Document {i+1}] Unknown Source")
            context += "---\n"

    prompt = f"{context}\nQuestion: {query}\nAnswer:"

    return prompt, citations

def generate_rag_answer(query, tokenizer, model, k_retrieval=3):
    """Performs RAG to generate an answer using retrieved documents and the LLM."""
    print(f"Retrieving documents for query: '{query}'...")
    # Use the vector retriever to get relevant documents
    retrieved_documents = vector_retriever.get_vector_retriever(query, k=k_retrieval)

    if not retrieved_documents:
        print("No relevant documents found.")
        return "Could not find relevant information to answer the query.", []

    # Build the prompt for the LLM
    prompt, citations = build_rag_prompt(query, retrieved_documents)

    print("Generating answer with LLM...")
    # Tokenize the prompt
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Generate response from the LLM
    # Using max_new_tokens instead of max_length for generation control
    outputs = model.generate(**inputs, max_new_tokens=150, num_beams=5, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Answer generated.")
    return answer, citations

# Example usage (optional - for testing)
if __name__ == "__main__":
    # Initialize LLM and tokenizer once
    llm_tokenizer, llm_model = initialize_llm_and_tokenizer(LLM_MODEL_NAME)

    print("\nSimple RAG Tool (Type 'quit' to exit)")
    while True:
        user_query = input("Enter your query: ")
        if user_query.lower() == 'quit':
            break

        # Generate RAG answer
        rag_answer, rag_citations = generate_rag_answer(user_query, llm_tokenizer, llm_model)

        print("\nRAG Answer:")
        print(rag_answer)

        if rag_citations:
            print("\nSources:")
            for citation in rag_citations:
                print(citation)

        print("\n" + "-"*20 + "\n") 