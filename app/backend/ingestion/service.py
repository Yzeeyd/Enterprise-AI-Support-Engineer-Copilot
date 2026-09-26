from pathlib import Path

from app.backend.ingestion.Loader import load_pdf_docs
from app.backend.ingestion.Chunker import split_documents

from app.backend.ingestion.document_tracker import (
    calculate_file_hash,
    get_document_id,
    get_document_status,
    load_index_state,
    save_index_state,
)


class IngestionService:

    def __init__(
        self,
        repository,
        documents_root: Path,
        state_path: Path,
    ):
        self.repository = repository
        self.documents_root = documents_root
        self.state_path = state_path

    def ingest_folder(self) -> dict:

        state = load_index_state(self.state_path)

        pdf_files = [
            file
            for file in self.documents_root.rglob("*.pdf")
            if file.is_file()
        ]

        results = {
            "new": [],
            "changed": [],
            "unchanged": [],
        }

        for file_path in pdf_files:

            status = self._ingest_file(
                file_path=file_path,
                state=state,
            )

            results[status].append(str(file_path))

        save_index_state(
            self.state_path,
            state,
        )

        return results

    def _ingest_file(
        self,
        file_path: Path,
        state: dict,
    ) -> str:

        document_id = get_document_id(
            str(file_path),
            str(self.documents_root),
        )

        current_hash = calculate_file_hash(
            str(file_path)
        )

        status = get_document_status(
            document_id=document_id,
            current_hash=current_hash,
            state=state,
        )

        if status == "unchanged":
            return status

        if status == "changed":

            old_chunk_ids = (
                state[document_id]
                .get("chunk_ids", [])
            )

            if old_chunk_ids:
                self.repository.delete_chunks(
                    old_chunk_ids
                )

        documents = load_pdf_docs(
            [str(file_path)]
        )

        chunks = split_documents(
            documents
        )

        chunk_ids = self.repository.index_chunks(
            chunks=chunks,
            document_id=document_id,
        )

        state[document_id] = {
            "hash": current_hash,
            "chunk_ids": chunk_ids,
        }

        return status