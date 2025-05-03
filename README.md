# SPADE-Smart-Personal-Assistant-for-Daily-Essentials
```
+------------------------------------------------------+
|     _______..______      ___       _______   _______ |
|    /       ||   _  \    /   \     |       \ |   ____||
|   |   (----`|  |_)  |  /  ^  \    |  .--.  ||  |__   |
|    \   \    |   ___/  /  /_\  \   |  |  |  ||   __|  |
|.----)   |   |  |     /  _____  \  |  '--'  ||  |____ |
||_______/    | _|    /__/     \__\ |_______/ |_______||
+------------------------------------------------------+
```
## Personal AI assistant
### Write a personal AI assistant that can:
  * Write and send emails on your behalf
  * Read multiple PDF files and answer questions
  * Schedule meetings for you
  * Search the Internet
  * Ask you questions, e.g., for your private information or when uncertain

### Key requirements
  * Do not leak your private information (use a local LLM instead)
  * Feel free to use any public LLM APIs for non-private data

### System requirements:
  * Ollama
  * Langchain/Langgraph/Langsmith (need to create langsmith api to monitor the program's responses)
  * Google Gmail/Calendar API service (need credentials files)
  * Conda environment/Python virtual environment: securely store the credentials for Google services or Langsmith's API key.

### How to run
  * Download an LLM from Ollama (the default is llama3.2)
    
    `ollama pull llama3.2`

  * Login to `console.cloud.google.com` and activate Gmail API and Calendar API
  * Download the credential and save it in /src folder (the default name is credentials.json)
  
  * Run the `assistant.py` script
    
    `python3 assistant.py`
