from modelsLangs import Model
from langchain_openai import ChatOpenAI

model: ChatOpenAI = Model("gpt-3.5-turbo").getOpenAIModel()
resposne = model.invoke("Who is the PM of India")
print(resposne)
