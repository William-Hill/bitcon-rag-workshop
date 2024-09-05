from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# Retrieve the GROQ_API_KEY from the environment
groq_api_key = os.getenv("GROQ_API_KEY")

#Change the prompt template from telling a joke to teaching you about a topic. We will see
#a demostration of the LLM hallucinating on topics outside of its training data

llm = ChatGroq(model_name="llama3-8b-8192")
prompt = ChatPromptTemplate.from_template("Teach about this {topic}")

chain = prompt | llm | StrOutputParser()

user_message = input("Enter a topic to learn about: ")
print(chain.invoke({'topic': user_message}))
