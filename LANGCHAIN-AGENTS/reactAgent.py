from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from modelsLangs import Model
from langchain_openai import ChatOpenAI

prompt = hub.pull("hwchase17/react")

model: ChatOpenAI = Model("gpt-3.5-turbo").getOpenAIModel()

tool_search = DuckDuckGoSearchRun()
tools_list = []
react_Agent = create_react_agent(llm=model, prompt=prompt, tools=tools_list)

agent_exec = AgentExecutor(agent=react_Agent, tools=tools_list, verbose=True)

response = agent_exec.invoke({"input": "Who is the current Pm of India"})
print(response)
