# from langchain_ollama import ChatOllama
# from langgraph.prebuilt import create_react_agent
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

class GmailTool:
    def __init__(self):
        # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
        # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
        self.credentials = get_gmail_credentials(
            token_file="src/token.json",
            scopes=["https://mail.google.com/"],
            client_secrets_file="src/credentials.json",
        )
        self.api_resource = build_resource_service(credentials=self.credentials)
        self.toolkit = GmailToolkit(api_resource=self.api_resource)

    def get_tools(self):
        return self.toolkit.get_tools()
    
    def get_toolkit(self):
        return self.toolkit
    


# gmail_toolkit = None

# def gmail_toolkit_init():
#     credentials = get_gmail_credentials(
#         token_file="token.json",
#         scopes=["https://mail.google.com/"],
#         client_secrets_file="credentials.json",
#     )
#     api_resource = build_resource_service(credentials=credentials)
#     gmail_toolkit = GmailToolkit(api_resource=api_resource)

# def gmail_get_tools():
#     return gmail_toolkit.get_tools()

# tools = gmail_toolkit.get_tools()
# print(tools)
# llm_model = ChatOllama(model="mistral:7b-instruct")
# agent_executor = create_react_agent(llm_model, tools)

# example_query = "Draft an email to kevin.tieu@tamu.edu thanking him for the help."

# events = agent_executor.stream(
#     {"messages": [("user", example_query)]},
#     stream_mode="values",
# )
# for event in events:
#     event["messages"][-1].pretty_print()