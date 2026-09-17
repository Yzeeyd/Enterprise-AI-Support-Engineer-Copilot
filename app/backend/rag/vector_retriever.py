
from app.backend.vector_store.chroma import get_vector_store
from app.backend.embeddings import get_embeddings_model

def similarity_search(query: str, top_k: int = 5):
    """
    Perform a similarity search using the vector store.

    Args:
        query (str): The query string to search for.
        top_k (int): The number of top results to return.

    Returns:
        list: A list of the top_k most similar documents.
    """
    
    embedding_model = get_embeddings_model()
    vector_store = get_vector_store(embedding_model)
    results = vector_store.similarity_search(query,k=top_k)
    return results


if __name__ == "__main__":
    # Example usage
    query = "كلمة السر"
    top_k = 5
    results = similarity_search(query, top_k=top_k)
    print(f"Top {top_k} results for query '{query}':")
    for result in results:
        print(result)

