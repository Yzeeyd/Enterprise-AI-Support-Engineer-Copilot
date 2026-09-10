from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
import json 
from document_tracker import calculate_file_hash, get_document_id, file_exists, load_index_state, get_document_status



def load_pdf_docs(pdf_paths: list[str] | None = None) -> list[Document]:
    """Load PDF documents and return them as a list of Document objects.
    
    args:
        pdf_paths (list[str] | None): List of PDF file paths to load. If None, it will load all PDF files in the default folder.
    returns:
        list[Document]: List of loaded Document objects.
    """
    docs: list[Document] = []
    for path in pdf_paths:
        file_path = Path(path)

        loader = PyPDFLoader(str(file_path))

        documents = loader.load()

        file_hash = calculate_file_hash(str(file_path))
        document_id = get_document_id(str(file_path), "data")

        for doc in documents:
            doc.metadata.update({
                "source": str(file_path),
                "filename": file_path.name,
                "file_type": "pdf",
                "hash": file_hash,
                "document_id": document_id
            })

        docs.extend(documents)
    return docs

if __name__ == "__main__":
    # Example usage
    folder_path = Path("data/raw/doc")

    pdf_paths = [str(file.resolve()) for file in folder_path.rglob("*.pdf")]

    loaded_docs = load_pdf_docs(pdf_paths)
    for doc in loaded_docs:
        print(f"Loaded document: {doc.metadata['filename']} with hash: {doc.metadata['hash']} and document ID: {doc.metadata['document_id']}")