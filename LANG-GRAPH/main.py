from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from typing import Annotated, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START ,END
from langgraph.graph.message import add_messages
from langchain_core.messages.base import BaseMessage
from state import State
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "false"
#os.environ["LANGCHAIN_PROJECT"] = "LANGG"

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="Gemma2-9b-It", api_key= os.getenv("GROQ_API_KEY"))
print(llm)

def chatbot(state: State)->BaseMessage:
    msg:BaseMessage = llm.invoke(state['messages'])
    msg_dict:dict[str,any]= {"messages":msg}
    return msg  



if __name__ == "__main":
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot",chatbot)
    graph_builder.add_edge(START,"chatbot")
    graph_builder.add_edge("chatbot",END)
    graph = graph_builder.compile()