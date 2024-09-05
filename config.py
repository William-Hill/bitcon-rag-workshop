import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Retrieve the GROQ_API_KEY from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM instances
# Llama 3 70B: A large language model with 70 billion parameters, offering high performance and versatility
LLM_LLAMA70B = ChatGroq(model_name="llama3-70b-8192")

# Llama 3 8B: A smaller version of Llama 3 with 8 billion parameters, balancing performance and efficiency
LLM_LLAMA8B = ChatGroq(model_name="llama3-8b-8192")

# Gemma 2 9B: Google's 9 billion parameter model, known for its efficiency and strong performance on various tasks
LLM_GEMMA2 = ChatGroq(model_name="gemma2-9b-it")

# Mixtral 8x7B: A mixture of experts model with 8 expert sub-models, each with 7 billion parameters,
# offering strong performance across a wide range of tasks
LLM_MIXTRAL = ChatGroq(model_name="mixtral-8x7b-32768")