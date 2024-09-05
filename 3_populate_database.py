# Import necessary modules from LangChain and other libraries
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings

# This script adds the NBA Collective Bargaining Agreement (CBA) to the ChromaDB Vector Database
# ChromaDB is a vector database that allows for efficient similarity search

# Define paths for the Chroma database and data storage
CHROMA_PATH = "chroma_nba_cba"  # Path where the Chroma database will be stored
DATA_PATH = "data_nba_cba"  # Path where the source data is located

def get_embedding_function():
    """
    Create and return an embedding function using Ollama's nomic-embed-text model.
    This function will be used to generate embeddings for the document chunks.
    Embeddings are vector representations of text that capture semantic meaning.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def load_documents():
    """
    Load the NBA CBA PDF document using PyPDFLoader.
    PyPDFLoader is used to extract text content from PDF files.
    Returns a list of Document objects, where each Document represents a page or section of the PDF.
    """
    loader = PyPDFLoader("nba_data/2023-NBA-Collective-Bargaining-Agreement.pdf")
    return loader.load()

def split_documents(documents: list[Document]):
    """
    Split the documents into smaller chunks for more effective processing and storage.
    This is crucial for RAG systems as it allows for more granular retrieval of relevant information.
    
    Args:
        documents (list[Document]): List of Document objects to be split.
    
    Returns:
        list[Document]: List of smaller Document chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,  # Number of characters per chunk
        chunk_overlap=80,  # Number of overlapping characters between chunks, helps maintain context
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    """
    Add the document chunks to the Chroma vector store.
    This function creates or updates a Chroma database with the document chunks.
    
    Args:
        chunks (list[Document]): List of Document chunks to be added to the database.
    """
    # Initialize or load the existing Chroma database
    # The embedding function is used to convert text chunks into vector representations
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=get_embedding_function()
    )
    # Add the new document chunks to the database
    # Each chunk will be embedded and stored for future similarity searches
    db.add_documents(chunks) 
    # Persist the changes to disk
    # This ensures that the database is saved and can be reloaded in future sessions
    db.persist()

def main():
    """
    Main function to orchestrate the process of loading, splitting, and storing documents.
    This function ties together all the steps required to populate the Chroma database.
    """
    # Load the PDF document
    documents = load_documents()
    # Split the documents into smaller chunks
    chunks = split_documents(documents)
    # Add the chunks to the Chroma vector store
    add_to_chroma(chunks)

if __name__ == "__main__":
    main()
