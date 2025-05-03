from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI
# import os

OPTIONS = {
    "llama": "llama3.2",
    "mistral": "mistral:7b-instruct",
    "qwen": "qwen2.5",
}
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Function to get the model based on user choice from Ollama
def get_model(model_choice: str = "llama"):
    # Check if the model choice is valid
    if model_choice not in OPTIONS:
        raise ValueError(f"Model choice '{model_choice}' is not valid. Choose from {list(OPTIONS.keys())}.")
    model_id = OPTIONS[model_choice]
    llm_model = ChatOllama(model=model_id, temperature=0.0)
    # llm_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    print(f"Model '{model_choice}' loaded with ID: {model_id}")
    return llm_model