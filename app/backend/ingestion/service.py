from pathlib import Path

from app.backend.ingestion.Loader import (
    load_pdf_docs
)

from app.backend.ingestion.Chunker import (
    split_documents
)

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

        state = load_index_state(
            self.state_path
        )

        pdf_files = sorted(
            file
            for file
            in self.documents_root.rglob(
                "*.pdf"
            )
            if file.is_file()
        )

        results = {
            "new": [],
            "changed": [],
            "reindexed": [],
            "unchanged": [],
            "deleted": []
        }

        current_document_ids = set()

        for file_path in pdf_files:

            document_id = get_document_id(
                str(file_path),
                str(self.documents_root)
            )

            current_document_ids.add(
                document_id
            )

            status = self._ingest_file(
                file_path=file_path,
                document_id=document_id,
                state=state
            )

            results[status].append(
                document_id
            )

        # Documents removed from source folder
        stale_documents = (
            set(state.keys())
            - current_document_ids
        )

        for document_id in stale_documents:

            if self.repository.document_exists(
                document_id
            ):
                self.repository.delete_document(
                    document_id
                )

            state.pop(
                document_id,
                None
            )

            results["deleted"].append(
                document_id
            )

        save_index_state(
            self.state_path,
            state
        )

        self.repository.refresh()

        return results


    def _ingest_file(
        self,
        file_path: Path,
        document_id: str,
        state: dict
    ) -> str:

        current_hash = calculate_file_hash(
            str(file_path)
        )

        status = get_document_status(
            document_id=document_id,
            current_hash=current_hash,
            state=state
        )

        exists_in_opensearch = (
            self.repository
            .document_exists(
                document_id
            )
        )

        # State + OpenSearch agree
        if (
            status == "unchanged"
            and exists_in_opensearch
        ):
            return "unchanged"

        # State says unchanged but
        # OpenSearch lost the document
        if (
            status == "unchanged"
            and not exists_in_opensearch
        ):
            status = "reindexed"

        # Remove previous chunks if any.
        if exists_in_opensearch:

            self.repository.delete_document(
                document_id
            )

        documents = load_pdf_docs(
            [str(file_path)]
        )

        # One canonical document_id.
        for document in documents:

            document.metadata.update({
                "document_id":
                    document_id,

                "hash":
                    current_hash
            })

        chunks = split_documents(
            documents
        )

        self.repository.index_chunks(
            chunks=chunks,
            document_id=document_id
        )

        state[document_id] = {
            "hash": current_hash
        }

        return status