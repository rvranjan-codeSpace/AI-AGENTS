from dotenv import load_dotenv
from langgraph.graph import Graph
import os
from langchain import hub
import json
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage, FunctionMessage
from langgraph.prebuilt import ToolExecutor, ToolInvocation, ToolNode
from langchain_groq import ChatGroq
from typing import Annotated, Dict, Any, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_community.tools import OpenWeatherMapQueryRun
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.schema import BaseOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from typing import Sequence
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
import operator
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents import create_react_agent, AgentExecutor
from langgraph.graph import StateGraph


import pprint

load_dotenv()


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPENWEATHERMAP_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
model = ChatGroq(model="Gemma2-9b-It", api_key=os.getenv("GROQ_API_KEY"))
# model = HuggingFaceEndpoint(repo_id='Gemma2-9b-It',model_kwargs={'temprature':0.6})


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


weather_query = OpenWeatherMapQueryRun()

wiki_api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=wiki_api_wrapper)
resp = wiki.invoke("Who is shahrukh khan in india?")

tools = [weather_query,wiki]
openai_functions = [convert_to_openai_function(t) for t in tools]
llm_with_tools = model.bind_functions(openai_functions)
tool_executor = ToolExecutor(tools=tools)


def agent_node(state):
    user_input = state["messages"]
    response = llm_with_tools.invoke(user_input)
    state["messages"].append(response)
    return {"messages": [response]}


def tool_node(state):
    messages = state["messages"]
    last_message = messages[-1]

    tool_name = last_message.additional_kwargs["function_call"]["name"]
    tool_input = json.loads(
        last_message.additional_kwargs["function_call"]["arguments"]
    )["location"]

    # construct a tool invocation from function call and pass the tool details to openweatherAPI
    action = ToolInvocation(tool=tool_name, tool_input=tool_input)

    # call the tool executor to get back the response
    response = tool_executor.invoke(action)

    # use the response to get the Functional Message
    function_message = FunctionMessage(content=str(response), name=action.tool)
    state["messages"].append((function_message))
    return {"messages": [function_message]}


def wiki_node(state):
    user_questions = state["messages"][0].content
    messages = state["messages"]
    last_message = messages[-1]
    tool_name = last_message.additional_kwargs["function_call"]["name"]
     # construct a tool invocation from function call and pass the tool details to openweatherAPI
    action = ToolInvocation(tool=tool_name, tool_input=user_questions)

    # call the tool executor to get back the response
    response = tool_executor.invoke(action)
    state["messages"].append((response))
    return {"messages": [response]}


def node_decison_maker(state):
    messages = state["messages"]
    last_message = messages[-1]
    # when we ask the llm not realted to weather : like who is Shahrukh khan ? or how are you. The the LLm gives below output in AI mEssage
    # London,GB is seen in location
    # {'arguments': '{"location":"London,GB"}'
    tool_input = ""
    tool_name = last_message.additional_kwargs["function_call"]["name"]
    if tool_name in "open_weather_map":
        return "continue"
    if tool_name in "wikipedia":
        return "wiki"


def agent_final_response(state: Dict[str, List[Any]]):
    weather_details = state["messages"][-1].content
    user_questions = state["messages"][0].content
    prompt = f"""
    From the weather details provided as following ${weather_details}
    Extract the answer based on the following questions:${user_questions}.
    your answer should be a one liner. Do not hallucinate and provide your own answer
    """
    response = model.invoke(prompt)
    state["messages"].append(response.content.rstrip())
    return {"messages": [response.content.rstrip()]}


def callGraph():
    workflow = StateGraph(state_schema=AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("responder", agent_final_response)
    workflow.add_node("wiki_node", wiki_node)

    # We need to pass a conditional edge for the agent node to decide where to go.
    # if its a quesiton that requires weather API then the flow should be to the graph
    # if the quesiton is generic then we can pass it to a tool like wiki pedia
    # Based on the  return "END" or "CONTINUE" we decide where to go

    workflow.add_conditional_edges(
        source="agent",
        path=node_decison_maker,
        path_map={"continue": "tool", "wiki": "wiki_node"},
    )

    # Below is the normal edge. This is not the conditional edge

    #workflow.add_edge("agent", "tool")
    workflow.add_edge("tool", "responder")
    #workflow.add_edge("agent","wiki_tool")
    workflow.set_entry_point("agent")
    app = workflow.compile()

    inputs = {"messages": [HumanMessage(content="Who is shahrukh khan in india?")]}
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Output from {key}:")
            print("-----")
            print(value)
            print("\n-----\n")
        output


callGraph()
