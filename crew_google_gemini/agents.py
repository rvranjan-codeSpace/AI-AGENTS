from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent
from Models import GoogleModel
from my_tools import my_serper_tool


class MyAgent:

    def __init__(self ):
        pass

    def getCrewAIAgentResarcher(self):
        model_name:str= "gemini-1.5-flash"
        google_llm =GoogleModel(model_name).getGoogleLLM()
        my_agent =Agent(
            role = "Senior Researcher",
            goal = "Uncover ground breaking reality in {topic}",
            verbose = True,
            memory = True,
            backstory=(
                "Drivern by cuorsity you are the forefornt of "
                "innovation, eager to explore and share knowledge that could change"
                "the world"
                ),
            tools=[my_serper_tool],
            llm= google_llm,
            allow_delegation=True
            )

    # create write agent with custom tools repsosible in writing news blog    
    def getCrewAIAgentWriter(self):

        model_name:str= "gemini-1.5-flash"
        google_llm =GoogleModel(model_name).getGoogleLLM()
        my_agent =Agent(
            role = "Writer",
            goal = "Narrate compelling story about the {topic}",
            verbose = True,
            memory = True,
            backstory=(
                "With a flair of simplifying complex topic, you craft "
                "engaging narrative that captivated and educate ,bringing new "
                "discoveris to light in accessible manner"
                ),
            tools=[my_serper_tool], 
            llm= google_llm,
            allow_delegation=False
            )
        

    






