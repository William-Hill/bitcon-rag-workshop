# Create Your Own ChatGPT For Fun and Profit - BITCON 2024

This repository contains a simple LangChain-based chat application that generates jokes based on user input.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/William-Hill/bitcon-rag-workshop.git
   cd bitcon-rag-workshop
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Get a Groq API Key:
   - Sign up for an account at [Groq](https://www.groq.com/)
   - Generate an API key from your account dashboard

5. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

6. Install Ollama:
   - Follow the instructions at [Ollama's official website](https://ollama.ai/) to install Ollama for your operating system.
   - Run the following command to download the required models:
     ```
     ollama pull llama3
     ollama pull nomic-embed-text
     ```

7. Populate the ChromaDB database:
   ```
   python 3_populate_database.py
   ```

## Tools and Libraries Used

1. **Ollama**: A local LLM runner that allows you to use various open-source models.

2. **CrewAI**: A framework for building AI agents that can work together to accomplish tasks.

3. **ChromaDB**: A vector database used for efficient similarity search in the NBA CBA document.

4. **Groq**: A cloud AI platform used for accessing powerful language models.

5. **LangChain**: A framework for developing applications powered by language models.

## Available Scripts

- `1_langchain_chat.py`: A simple chat interface using LangChain and Ollama.
- `2_langchain_chat_cba.py`: A streaming chat interface for querying the NBA CBA.
- `3_populate_database.py`: Script to populate the ChromaDB with NBA CBA data.
- `4_nba_rag.py`: A Retrieval-Augmented Generation (RAG) system for querying the NBA CBA.
- `6_nba_agent_rag.py`: An agent-based system using CrewAI for retrieving NBA all-time leader statistics.

## Usage

Run the desired script using Python. For example:

```
python 1_langchain_chat.py
```

