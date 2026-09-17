from pathlib import Path
import os
#search
from app.backend.search.client import get_opensearch_client
from app.backend.search.index import create_index
from app.backend.search.repository import OpenSearchRepository
#embeddings
from app.backend.embeddings.ollama import get_embeddings_model
#ingestion
from app.backend.ingestion.Loader import load_pdf_docs
from app.backend.ingestion.Chunker import split_documents
from app.backend.ingestion.document_tracker import calculate_file_hash, get_document_id, load_index_state, get_document_status,save_index_state
#rag
from app.backend.rag.vector_retriever import VectorRetriever

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

    embeddings = get_embeddings_model()
    client = get_opensearch_client()

    probe_vector = embeddings.embed_query("dimension probe")
    create_index(
        client=client,
        embedding_dimension=len(probe_vector)
    )

    repository = OpenSearchRepository(
        client=client,
        embedding_model=embeddings
    )

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
            chunk_ids = repository.index_chunks(
                chunks=chunks,
                document_id=document_id
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
                repository.delete_chunks(old_chunk_ids)

            documents = load_pdf_docs([file_path])
            chunks = split_documents(documents)

            new_chunk_ids = repository.index_chunks(
                chunks=chunks,
                document_id=document_id
                )

            state[document_id] = {
                "hash": current_hash,
                "chunk_ids": new_chunk_ids
            }

        
        
    save_index_state(state_path, state)

    
if __name__ == "__main__":
    index_documents_pipeline()