# Import necessary modules from LangChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
import sys

# Define a custom callback handler to stream output
# This is used to avoid duplicate characters that can occur with the default streaming handler
class StreamHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """
        This method is called every time the LLM produces a new token.
        
        Args:
            token (str): The new token produced by the LLM.
            **kwargs: Additional keyword arguments (not used in this implementation).
        
        The method writes each token directly to stdout and flushes immediately,
        ensuring real-time, non-buffered output. This approach prevents the
        duplication of characters that can occur with some default streaming handlers.
        """
        # Write each token directly to stdout without buffering
        sys.stdout.write(token)
        # Flush immediately to ensure real-time output
        sys.stdout.flush()

# Initialize the ChatOllama model with streaming enabled
llm = ChatOllama(model='llama3.1', streaming=True)

# Create a ChatPromptTemplate for generating educational content
# This template takes a 'topic' parameter to customize the learning subject
prompt = ChatPromptTemplate.from_template("Teach me about {topic}")

# Create a processing chain:
# 1. Start with the prompt template
# 2. Pass it to the language model (llm)
# Note: We don't use StrOutputParser here as it's not needed for streaming
chain = prompt | llm

# Get user input for the learning topic
user_message = input("Enter a topic to learn about: ")

# Invoke the chain with the user's topic and our custom StreamHandler
# The custom handler ensures smooth, non-duplicated streaming output
chain.invoke({'topic': user_message}, config={'callbacks': [StreamHandler()]})

# Print a newline at the end for better formatting
print()
