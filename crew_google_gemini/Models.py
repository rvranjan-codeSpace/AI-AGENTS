from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
class Model:
    def __init__(self,name, temprature=0.5):
        self.temprature = 0.5
        self.name = name

class OpenAIModel(Model):
    def __init__(self, name, temprature:None):
        if temprature is None:
            self.temprature = temprature
        super().__init__(name, temprature)
        load_dotenv()
        os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')


class GoogleModel(Model):
    def __init__(self, name, temprature, verbose):
        if temprature is not None:
            self.temprature = temprature
        if verbose is None: 
            self.verbose = True
        super().__init__(name, temprature)

    def getGoogleLLM(self):
        return ChatGoogleGenerativeAI(model=self.name,
                                     verbose=self.verbose,
                                     temperature=self.temprature,
                                     api_key=os.getenv('GOOGLE_API_KEY')
                                     )



