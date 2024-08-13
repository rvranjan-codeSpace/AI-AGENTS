from dotenv import load_dotenv
from typing import Union
from langchain.agents import tool
from langchain.tools.render import render_text_description
from langchain.tools import Tool
from langchain.schema import AgentAction, AgentFinish
from langchain import hub
from langchain.prompts import PromptTemplate
import pprint
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from modelsLangs import Model
from typing import List, Tuple
from agentcallback import AgentCallBackHandler
from langchain.agents.format_scratchpad import format_log_to_str


@tool
def get_text_len(text: str) -> int:
    """Return the length of the given string"""
    print(f"Getting text length entered with {text} ")
    clean_text = text.strip("'\n")
    return len(clean_text)


def find_tool_from_tool_list(tools_list: List[Tool], tool_name: str) -> Tool:
    tool_to_use = next((t for t in tools_list if t.name == tool_name), None)
    if tool_to_use is None:
        raise ValueError(f"tool_name {tool_name} not found")
    return tool_to_use


def find_tool_to_use(tools_list: List[Tool], tool_name: str) -> Tool:
    for t in tools_list:
        if t.name == tool_name:
            tool_to_use = t
        else:
            ValueError(f"tool_name{tool_name} not found")
    return tool_to_use


def format_log_to_str(
    intermediate_steps: List[Tuple[AgentAction, str]],
    observation_prefix: str = "Observation: ",
    llm_prefix: str = "Thought: ",
) -> str:
    """Construct the scratchpad that lets the agent continue its thought process.

    Args:
        intermediate_steps: List of tuples of AgentAction and observation strings.
        observation_prefix: Prefix to append the observation with.
             Defaults to "Observation: ".
        llm_prefix: Prefix to append the llm call with.
                Defaults to "Thought: ".

    Returns:
        str: The scratchpad.
    """
    thoughts = ""
    for action, observation in intermediate_steps:
        thoughts += action.log
        thoughts += f"\n{observation_prefix}{observation}\n{llm_prefix}"
    return thoughts


if __name__ == "__main__":
    my_tools = [get_text_len]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """
    tools_desc = render_text_description(tools=my_tools)
    # There are two ways of defining the prompt. first ist thorugh partal method and second is throguh partial_varaibles
    # prompt = PromptTemplate.from_template(template=template,partial_variables={"tools":[get_text_len],"tool_names":"get_text_len"})

    # second way of defining the prompt
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=tools_desc, tool_names=",".join([t.name for t in my_tools])
    )
    # pprint.pp("PROMPT:")
    # pprint.pp(prompt)
    print("\n\n Starting...")
    stop_sequences = ["Observation", "Observation:"]
    llm = Model(name="gpt-3.5-turbo").getOpenAIModel(
        temperature=0, stop_args=stop_sequences, callbacks_args=AgentCallBackHandler()
    )
    intermediate_step = []
    agent_chain = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda y: format_log_to_str(y["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_response = ""

    while not isinstance(agent_response, AgentFinish):
        agent_response: Union[AgentAction, AgentFinish] = agent_chain.invoke(
            {
                "input": "what is the lenght of 'DOG' in chatacters?",
                "agent_scratchpad": intermediate_step,
            }
        )
        print(agent_response)

        if isinstance(agent_response,AgentAction):
            tool_name: str = agent_response.tool
            tool_to_use: Tool = find_tool_from_tool_list(my_tools, tool_name)
            tool_input: Union[str, dict] = agent_response.tool_input
            observation = tool_to_use.func(str(tool_input))
            print(f"Observation={observation}")
            intermediate_step.append((agent_response, str(observation)))

    if isinstance(agent_response, AgentFinish):
        print(agent_response)
