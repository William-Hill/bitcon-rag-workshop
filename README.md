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

4. Install Ollama and download the Llama 3 model:
   - Follow the instructions at [Ollama's official website](https://ollama.ai/) to install Ollama for your operating system.
   - Run the following command to download the Llama 3 model:
     ```
     ollama pull llama3
     ```

5. Run the application:
   ```
   python 1_langchain_chat.py
   ```

6. Enter a topic when prompted, and the application will generate a joke about that topic.

## Note

Make sure you have Python 3.7 or later installed on your system.
