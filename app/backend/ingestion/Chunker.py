from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """Split documents into smaller chunks.
    
    args:
        documents (list[Document]): List of Document objects to split.
        chunk_size (int): Maximum size of each chunk.
        chunk_overlap (int): Number of characters to overlap between chunks.
    
    returns:
        list[Document]: List of split Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)