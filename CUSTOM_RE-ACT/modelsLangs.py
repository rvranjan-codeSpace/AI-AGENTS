from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


class Model:
    def __init__(self, name):
        self.name = name
        self._temperature = 0.5

    def getOpenAIModel(
        self, stop_args=None, temperature=None, callbacks_args=None
    ) -> ChatOpenAI:
        load_dotenv()  # Ensure environment variables are loaded
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        callbacks_args = callbacks_args if callbacks_args else None

        if temperature is not None:
            self._temperature = temperature

        stop_sequences = stop_args if stop_args else None
        open_ai_model_debug = ChatOpenAI(
            model=self.name,
            temperature=self._temperature,
            stop=stop_sequences,
            callbacks=[callbacks_args],
        )
        return open_ai_model_debug
