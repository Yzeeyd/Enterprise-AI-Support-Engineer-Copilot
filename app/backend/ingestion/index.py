from dotenv import load_dotenv
from pathlib import Path
import os

from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

from Loader import load_pdf_docs
from Chunker import split_documents
from service import VectorStore

if __name__ == "__main__":

    # Load PDF documents
    folder_path = Path(os.getenv("ABSALUTEPATH")) / "data" / "raw" / "doc"

    # Get all file paths in the folder and its subfolders
    file_paths = [str(file.resolve()) for file in folder_path.rglob("*") if file.is_file()]

    docs = load_pdf_docs(file_paths)
    docs_chunks = split_documents(docs)

    embeddings_model = OllamaEmbeddings(model="qwen3-embedding:latest")
    vector_store = VectorStore(embeddings_model)
    for chunk in docs_chunks:
        vector_store.add_texts([chunk.page_content], metadatas=[chunk.metadata])
    
    results = vector_store.similarity_search("كلمة المرور", k=3)
    for result in results:
        print(result.metadata)
        print(result.page_content)
        print("--------------------------------------------------")
