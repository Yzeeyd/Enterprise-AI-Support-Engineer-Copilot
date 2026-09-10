from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


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

        for doc in documents:
            doc.metadata.update({
                "source": str(file_path),
                "filename": file_path.name,
                "file_type": "pdf",
            })

        docs.extend(documents)
    return docs