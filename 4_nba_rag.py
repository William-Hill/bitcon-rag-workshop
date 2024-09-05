import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings

# This script creates a Retrieval-Augmented Generation (RAG) application to query the NBA Collective Bargaining Agreement (CBA)
# Note: Run the 3_populate_database.py script first to add the CBA PDF to ChromaDB

# Path to the Chroma database containing the CBA data
CHROMA_PATH = "chroma_nba_cba"

# Template for the prompt to be sent to the language model
# It includes placeholders for the context (retrieved from the database) and the user's question
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def get_embedding_function():
    """
    Create and return an embedding function using Ollama's nomic-embed-text model.
    This function is used to generate embeddings for both stored documents and user queries.
    """
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def query_rag():
    """
    Main function to handle the RAG query process.
    This function orchestrates the retrieval of relevant context and generation of the answer.
    """
    # Initialize the Chroma database with the embedding function
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Get the user's question
    user_message = input("Enter a question about the NBA CBA: ")

    # Perform a similarity search in the database to find relevant context
    # k=5 means we retrieve the top 5 most similar chunks
    results = db.similarity_search_with_score(user_message, k=5)

    # Combine the content of the retrieved documents into a single context string
    context_text = "\n\n----\n\n".join([doc.page_content for doc, _score in results])

    # Print the retrieved context (for debugging purposes)
    print("context_text:\n", context_text)

    # Create a ChatPromptTemplate using the defined template
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # Format the prompt with the retrieved context and user's question
    prompt = prompt_template.format(context=context_text, question=user_message)

    # Initialize the language model (Ollama with llama3 model)
    model = Ollama(model='llama3')

    # Generate a response using the language model
    response_text = model.invoke(prompt)

    print("Sending context to Llama3 to generate a response.....")

    # Print the generated response
    print("\n-----------------------------\n")
    print(response_text)
    print("\n-----------------------------\n")

# Execute the RAG query function
query_rag()
