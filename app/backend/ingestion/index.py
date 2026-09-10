from dotenv import load_dotenv
from pathlib import Path
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

from Loader import load_pdf_docs
from Chunker import split_documents
from service import VectorStore, embeddings_model
from document_tracker import calculate_file_hash, get_document_id, file_exists, load_index_state, get_document_status,save_index_state

load_dotenv()


def add_chunks_to_vector_store(chunks, vector_store):
    for chunk in chunks:
        vector_store.add_document(chunk)

def index_documents_Pipeline() -> None:
    """Index documents and update the index state."""

    folder_path = Path(os.getenv("DATAPATH")) / "raw" / "doc"
    file_paths = [str(file.resolve()) for file in folder_path.rglob("*.pdf") if file.is_file()]
    state_path = Path(os.getenv("DATAPATH")) / "index_state.json"

    embeddings_modelOllama = embeddings_model()    
    vector_store = VectorStore(embeddings_modelOllama)
    
    documents = load_pdf_docs(file_paths)
    docs_chunks = split_documents(documents)
    state = load_index_state(state_path)
    
    for doc in documents:
        document_id = doc.metadata["document_id"]
        current_hash = doc.metadata["hash"]
        status = get_document_status(document_id, current_hash, state)
        if status == "new":
                print(f"Indexing new document: {document_id}")
                # Add your indexing logic here
                add_chunks_to_vector_store(docs_chunks, vector_store)
                state[document_id] = {"hash": current_hash}
            elif status == "changed":
                print(f"Updating changed document: {document_id}")
                # Add your update logic here
                state[document_id] = {"hash": current_hash}
            else:
                print(f"Document unchanged: {document_id}")


    

    save_index_state(state_path, state)

if __name__ == "__main__":
    print("Starting the ingestion process...")

    

    index_documents_Pipeline()

    

    embeddings_modelOllama = embeddings_model()    
    vector_store = VectorStore(embeddings_modelOllama)
    print("Searching for similar documents...")
    results = vector_store.similarity_search("كلمة المرور", k=3)
    for result in results:
        print(result.metadata)
        print(result.page_content)
        print("--------------------------------------------------")
