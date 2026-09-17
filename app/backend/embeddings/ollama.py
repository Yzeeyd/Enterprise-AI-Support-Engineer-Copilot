from langchain_ollama import OllamaEmbeddings



def get_embeddings_model(model="qwen3-embedding:latest") -> object:
    """Create an embeddings model.
    
    args:
        None
    returns:
        An embeddings model object."""
    
    return OllamaEmbeddings(model=model)