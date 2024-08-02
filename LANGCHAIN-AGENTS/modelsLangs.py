from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
class Model:

    def __init__(self,name):
        self.name= name
        self._temperature  = 0.5

    def getOpenAIModel(self,temperature=None)->ChatOpenAI:
        load_dotenv()  # Ensure environment variables are loaded
        os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')
        if temperature is not None:
            self._temperature = temperature
        return ChatOpenAI(model=self.name,temperature=self._temperature)


        