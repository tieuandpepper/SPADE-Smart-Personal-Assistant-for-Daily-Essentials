import os, getpass, sys
import streamlit as st
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime
from zoneinfo import ZoneInfo
from langchain.tools import Tool
from model import get_model
from tools.email import GmailTool
from tools.calendar import CalendarTool
from tools.search import search_internet
from tools.database import create_database, add_to_database, retrieve_from_database, read_pdf
import warnings
import curses
# from langchain import LangChainDeprecationWarning
# warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "personal-assistant"

add_database_tool = Tool.from_function(
    func=add_to_database,
    name="add_to_database",
    description="Takes a JSON array string of {{source, text}} objects and adds them to the existing RAG database named my_database.",
)
retrieve_tool = Tool.from_function(
    func=retrieve_from_database,
    name="retrieve_from_database",
    description="Given a query string, returns the top-k relevant document excerpts from the RAG database named my_database.",
)

search_internet_tool = Tool.from_function(
    func=search_internet,
    name="search_internet",
    description="Search in real-time, get factual web results for a query.",
)

gmail_tools = GmailTool().get_tools()

calendar_tools = CalendarTool()

calendar_create_event_tool = Tool.from_function(
    func=calendar_tools.calender_create_event,
    name="calender_create_event",
    description="Create an event on Google Calendar. Takes a JSON string with summary, start_time, end_time."
)

calendar_check_event_conflict_tool = Tool.from_function(
    func=calendar_tools.calendar_check_conflict,
    name="calendar_check_event_conflict",
    description="check for a schedule conflict on Google Calendar. Takes a JSON string with summary, start_time, end_time."
)

tools = [search_internet_tool, retrieve_tool, add_database_tool, calendar_create_event_tool, calendar_check_event_conflict_tool]
tools.extend(gmail_tools)
# Bind to your Ollama model
llm = get_model("llama")
llm_with_tools = llm.bind_tools(tools)

current_time = datetime.now(ZoneInfo("America/Chicago"))
current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
day_of_week = current_time.strftime("%A")
current_msg = f"""
My name is Kevin and you are my helpful assistant. Today is {day_of_week}, {current_time_str}. Your current location is College Station, Texas.
You are tasked to help with managing emails, calendar, searching for relevant information and retrieving information from a RAG database.
Specifically, you can send emails, create an event on Google calendar, check for event conflict on the calendar, search the Internet for information, and retrieving personal data from RAG database.

General guidelines:
- Never assume information unless explicitly provided by the user.
- Always ask for details when they are missing or unclear.
- Always provide the exact details when calling tools, such as email addresses, time, date (relative terms like tomorrow, next hour are unacceptable).
- Clearly communicate which tool you are using and why.

Error handling:
- Provide clear explanation if a tool fails.
- Suugest alternative when appropriate.
- Ask for clarification if requests are ambiguous.
"""
# System message
sys_msg = SystemMessage(content=current_msg)

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()

# Specify a thread
config = {"configurable": {"thread_id": "active_thread"}}
app = builder.compile(checkpointer=memory)

# # Example query
# example_query = "Draft an email to kevin.tieu@tamu.edu asking him to review the code. send it now."
# messages = [HumanMessage(content=example_query)]
# # Run the graph
# messages = app.invoke({"messages": messages},config)

# for m in messages['messages']:
#     m.pretty_print()


USER_MSG = f"""
Today is {day_of_week}, {current_time_str}.

Howdy!

My name is SPADE, a Smart Personal Assistant for Daily Essentials. I am here to assist you with your daily tasks.
I can manage emails (send, create a draft, and search emails), schedule meetings, and search the Internet.
You can type 'exit' or 'quit' to stop'
"""
os.system('clear')
print(USER_MSG)
state_msgs = []
while True:
    # print(USER_MSG)
    try:
        user_input = input("\n\nUser: ")
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break
    if user_input.strip().lower() in ("exit", "quit"):
        print("Goodbye!")
        os.system('clear')
        break
    if user_input.strip().lower() == "clear":
        os.system('clear')
        print(USER_MSG)
        continue

    # Add the user's message to the conversation state
    state_msgs.append(HumanMessage(content=user_input))

    # Invoke the LangGraph assistant
    msgs = app.invoke({"messages": state_msgs}, config)
    # The last message in the returned state is the assistant's reply
    state_msgs.append(msgs["messages"][-1])
    assistant_msg = msgs["messages"][-1]
    assistant_msg.pretty_print()