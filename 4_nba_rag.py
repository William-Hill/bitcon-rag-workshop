import argparse
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings

#Creating a RAG application to be able to query the NBA Collective Bargaining Agreement (CBA)
#Need to run the 5_populate_database.py script first to add the CBA PDF to the ChromaDB first


CHROMA_PATH = "chroma_nba_cba"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings



def query_rag():
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    #Finish adding the RAG query below
    user_message = input("Enter a topic to learn about:")

    results = db.similarity_search_with_score(user_message, k=5)

    context_text = "\n\n----\n\n".join([doc.page_content for doc, _score in results])

    print("context_text:", context_text)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_template.format(context=context_text, question=user_message)

    model = Ollama(model='llama3')

    response_text = model.invoke(prompt)

    print("\n-----------------------------\n")
    print(response_text)
    print("\n-----------------------------\n")


query_rag()
