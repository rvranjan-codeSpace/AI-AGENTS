from langchain_community.tools import DuckDuckGoSearchRun
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor
from modelsLangs import Model
from langchain_openai import ChatOpenAI

model: ChatOpenAI = Model("gpt-3.5-turbo").getOpenAIModel()
# resposne = model.invoke("Who is the PM of India")
# print(resposne)


my_prompt = hub.pull("hwchase17/openai-functions-agent")
print(my_prompt)

tool_search = DuckDuckGoSearchRun()
tools_list = [tool_search]
my_agent = create_openai_functions_agent(llm=model, tools=tools_list, prompt=my_prompt)
agent_exec = AgentExecutor(agent=my_agent, tools=tools_list, verbose=True)

response = agent_exec.invoke({"input": "Who is the current Pm of India"})
print(response)
