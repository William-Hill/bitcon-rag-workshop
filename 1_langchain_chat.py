# Import necessary modules from LangChain
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the ChatOllama model
# This uses the locally running Ollama service with the 'llama3.1' model
llm = ChatOllama(model='llama3.1')

# Create a ChatPromptTemplate for generating jokes
# This template takes a 'topic' parameter to customize the joke
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")

# Create a processing chain:
# 1. Start with the prompt template
# 2. Pass it to the language model (llm)
# 3. Parse the output as a string
# The '|' operator is used to connect these components
chain = prompt | llm | StrOutputParser()

# Get user input for the joke topic
# This prompts the user to enter a subject for the joke
user_message = input("Enter a topic to make a joke about: ")

# Invoke the chain with the user's topic and print the result
# This generates a joke about the given topic using the LLM
# The 'invoke' method runs the entire chain, from prompt to output
print(chain.invoke({'topic': user_message}))
