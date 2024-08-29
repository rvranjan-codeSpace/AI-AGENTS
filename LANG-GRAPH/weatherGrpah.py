from dotenv import load_dotenv
from langgraph.graph import Graph
import os
from langchain_groq import ChatGroq
from typing import Annotated, Dict, Any, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START ,END
from langgraph.graph.message import add_messages
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.ai import AIMessage
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain.schema import BaseOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import pprint
load_dotenv()


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="Gemma2-9b-It", api_key= os.getenv("GROQ_API_KEY"))
os.environ["OPENWEATHERMAP_API_KEY"] = os.getenv("OPENWEATHERMAP_API_KEY")

def getCityName(state:Dict[str, List[Any]]):
    user_input = state.get("messages")[-1]
    prompt=f"""your job is to extract the city name from the user input. 
                 No other informaiton. Jus the city name. Here is the user input:{user_input}
             """
    response = llm.invoke(prompt)
    state["messages"].append(response.content.rstrip())
    #prompt_another_way = ChatPromptTemplate.from_template(prompt)
    #chain = prompt_another_way | llm | StrOutputParser()
    return state
    

def getWeatherDetails(state:Dict[str,List[Any]]):
    agent_response = state["messages"][-1]
    weather = OpenWeatherMapAPIWrapper()
    weather_details = weather.run(agent_response)
    state["messages"].append(weather_details)
    return state

def agent_final_response(state:Dict[str, List[Any]]):
    weather_details = state["messages"][-1]
    user_questions = state["messages"][0]
    prompt = f'''
    From the weather details provided as following ${weather_details}
    Extract the answer based on the following questions:${user_questions}.
    your answer should be a one liner. Do not hallucinate and provide your own answer
    '''
    response = llm.invoke(prompt)
    state["messages"].append(response.content.rstrip())
    return response.content.rstrip()

def callGraph():
    workflow = Graph()
    workflow.add_node("agent",getCityName)
    workflow.add_node("tool",getWeatherDetails)
    workflow.add_node("responder",agent_final_response)
    workflow.add_edge("agent","tool")
    workflow.add_edge("tool","responder")

    workflow.set_entry_point("agent")
    workflow.set_finish_point("responder")

    app = workflow.compile()
    
    inputs = {"messages":["What is the temprature of Kolkata"]}

    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Output from {key}:")
            print("-----")
            print(value)
            print("\n-----\n")
        output

callGraph()






