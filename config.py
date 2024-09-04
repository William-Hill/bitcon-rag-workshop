import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Retrieve the GROQ_API_KEY from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM instances
LLM_LLAMA70B = ChatGroq(model_name="llama3-70b-8192")
LLM_LLAMA8B = ChatGroq(model_name="llama3-8b-8192")
LLM_GEMMA2 = ChatGroq(model_name="gemma2-9b-it")
LLM_MIXTRAL = ChatGroq(model_name="mixtral-8x7b-32768")