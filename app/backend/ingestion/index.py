from dotenv import load_dotenv
from pathlib import Path
import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

from Loader import load_pdf_docs
from Chunker import split_documents
from service import VectorStore, embeddings_model,add_chunks_to_vector_store
from document_tracker import calculate_file_hash, get_document_id, file_exists, load_index_state, get_document_status,save_index_state

load_dotenv()




def index_documents_pipeline() -> None:

    data_path = Path(os.getenv("DATAPATH"))
    folder_path = data_path / "raw" / "doc"
    state_path = data_path / "index_state.json"

    file_paths = [
        str(file.resolve())
        for file in folder_path.rglob("*.pdf")
        if file.is_file()
    ]

    state = load_index_state(state_path)

    embeddings = embeddings_model()
    vector_store = VectorStore(embeddings)
    for file_path in file_paths:

        document_id = get_document_id(
            file_path,
            str(data_path)
        )

        current_hash = calculate_file_hash(file_path)

        status = get_document_status(
            document_id,
            current_hash,
            state
        )

        if status == "unchanged":
            print(f"Document unchanged: {document_id}")
            continue

        if status == "new":
            print(f"Indexing new document: {document_id}")

            documents = load_pdf_docs([file_path])
            chunks = split_documents(documents)

            chunk_ids = add_chunks_to_vector_store(
                chunks,
                vector_store,
                document_id
            )

            state[document_id] = {
                "hash": current_hash,
                "chunk_ids": chunk_ids
            }

        elif status == "changed":
            print(f"Updating changed document: {document_id}")
            old_chunk_ids = state[document_id].get(
                "chunk_ids",
                []
            )

            if old_chunk_ids:
                vector_store.delete(
                    ids=old_chunk_ids
                )

            documents = load_pdf_docs([file_path])
            chunks = split_documents(documents)

            new_chunk_ids = add_chunks_to_vector_store(
                chunks,
                vector_store,
                document_id
            )

            state[document_id] = {
                "hash": current_hash,
                "chunk_ids": new_chunk_ids
            }

        
        
    save_index_state(state_path, state)

    
if __name__ == "__main__":
    print("Starting the ingestion process...")

    index_documents_pipeline()

    embeddings_modelOllama = embeddings_model(model="qwen3-embedding:0.6b")    
    vector_store = VectorStore(embeddings_modelOllama)
    print("Searching for similar documents...")
    results = vector_store.similarity_search("كلمة المرور", k=1)
    for result in results:
        print(result.metadata)
        print(result.page_content)
        print("--------------------------------------------------")
