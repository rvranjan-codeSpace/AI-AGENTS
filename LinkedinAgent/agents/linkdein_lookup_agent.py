from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import sys
from langchain.tools import Tool
from langchain.prompts.prompt import PromptTemplate
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.tool import get_profile_with_url_Tavily

# print(os.path.dirname(__file__))
# res = os.path.join(os.path.dirname(__file__), '..')
# print(res)
# res1=os.path.abspath(res)
# print(res1)

from langchain_community.tools.tavily_search import TavilySearchResults


def lookup(name: str) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    prompt = """
    given th full name {name_of_person} I want you to get me a link to their linkedin profile page.
    your answer should contain the URL
    """
    prompt_template = PromptTemplate(
        template=prompt, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 Linkedin profile page",
            func=get_profile_with_url_Tavily,
            description="Returns the URL of the given linkeding profile by name",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    aget_exec = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = aget_exec.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    load_dotenv()  # Ensure environment variables are loaded
    # "https://www.linkedin.com/in/rajan-ranjan15/"
    linkedin_url = lookup("rajan-ranjan15")
    print(linkedin_url)
