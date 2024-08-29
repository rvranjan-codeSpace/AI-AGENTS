from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from typing import Annotated, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START ,END
from langgraph.graph.message import add_messages
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.ai import AIMessage
from state import State
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langgraph.prebuilt import ToolNode, tools_condition
from IPython.display import Image,display
import pprint
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "false"
#os.environ["LANGCHAIN_PROJECT"] = "LANGG"


llm = ChatGroq(model="Gemma2-9b-It", api_key= os.getenv("GROQ_API_KEY"))

 ### Arxiv and Wiki Wrapper
arxivWrapper = ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=200)
arxiv=ArxivQueryRun(api_wrapper=arxivWrapper)

wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
wiki= WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

def chatbot(state: State)->BaseMessage:
    print(state["messages"])
    msg:AIMessage = llm.invoke(state['messages'])
    temp = {"messages":[msg]}
    return temp 

def chatbot_with_tools(state: State)->BaseMessage:
    #print(wiki.invoke("what is Machine learning"))
    tools =[wiki]
    llm_tools= llm.bind_tools(tools=tools)
    #llm.with_structured_output()
    #print(state["messages"])
    msg:AIMessage = llm_tools.invoke(state['messages'])
    temp = {"messages":[msg]}
    return temp  
 
def simpleLLM():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot",chatbot)
    graph_builder.add_edge(START,"chatbot")
    graph_builder.add_edge("chatbot",END)
    graph = graph_builder.compile()
    try:
        print("displaying the graph")
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        pass
    while True:
        user_input = input("User:") 
        if user_input in ["quit","q"]:
            print("goodBye")
            break
        for event in graph.stream({'messages':("user", user_input)}):
            for value in event.values():
                print("Assistant:",value["messages"][-1].content)

def llm_with_Tools():
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot",chatbot_with_tools)
    tools=[wiki]
    tool_node = ToolNode(tools = tools)
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges("chatbot", tools_condition)

    graph_builder.add_edge("tools","chatbot")
    graph_builder.add_edge(START,"chatbot")
    #graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile()
    print(graph.config_specs)
    #Execute the code
    user_input =  "WHo is shahrukh khan?"
    events= graph.stream(
        {
            "messages":[("user",user_input)]
        },
        stream_mode="values"
    )

    for event in events:
            pprint.pprint(event["messages"][-1])

if __name__ == "__main__":
    #simpleLLM()
    llm_with_Tools()    
    
  

