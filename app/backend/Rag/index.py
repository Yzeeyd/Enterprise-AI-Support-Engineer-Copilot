from dotenv import load_dotenv
from pathlib import Path
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
load_dotenv()

def load_langchain_docs(doc_paths: list[str] | None = None) -> list[Document]:
    """Fetch LangChain documentation pages as Documents."""

    docs: list[Document] = []
    for path in doc_paths:
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

folder_path = Path("Enterprise-AI-Support-Engineer-Copilot-AWS/app/backend/Rag/doc")

file_paths = [str(file.resolve()) for file in folder_path.rglob("*") if file.is_file()]

docs = load_langchain_docs(file_paths)
print(f"Loaded {len(docs)} documentation pages.")

print(type(docs))
print(type(docs[0]))

print("\nCONTENT:")
print(docs[0].page_content[:500])

print("\nMETADATA:")
print(docs[0].metadata)