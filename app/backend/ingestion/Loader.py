from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader
)


def load_pdf_docs(
    pdf_paths: list[str]
) -> list[Document]:

    docs: list[Document] = []

    for path in pdf_paths:

        file_path = Path(path)

        loader = PyPDFLoader(
            str(file_path)
        )

        documents = loader.load()

        for doc in documents:

            doc.metadata.update({
                "source": file_path.as_posix(),
                "filename": file_path.name,
                "file_type": "pdf"
            })

        docs.extend(documents)

    return docs