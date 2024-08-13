from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
from third_party.linkedin_scraper import getLinkedinDetails
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from agents.linkdein_lookup_agent import lookup
from outputParsers.summaryParser import summary_parser


def iceBreaker() -> any:
    print("Starting Ice breaker...")
    user_name = lookup("rajan-ranjan15")

    # getLinkedinDetails(url) :is the proxy wau to get linkeidn details.
    # getLinkedinDetails(user_name) : Its not able to login to the linkedin and hence not able to get the content
    # linkeding_content= getLinkedinDetails(user_name)
    linkeding_content = getLinkedinDetails(
        "https://www.linkedin.com/in/rajan-ranjan15/"
    )

    template = """
        Given the information entire details from a linkeding profile as: {information}
        I want you to create
        1)Summary of the profile
        2) 2 uniqe quaities \n
        {format_instruction}
    """
    myPromt = PromptTemplate(
        input_variables="information",
        template=template,
        partial_variables={
            "format_instruction": summary_parser.get_format_instructions()
        },
    )
    print(f"MY PROMPT={myPromt}")
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    # chain  = myPromt | llm | StrOutputParser()
    chain = myPromt | llm | summary_parser
    result = chain.invoke({"information": linkeding_content})
    print(result)


if __name__ == "__main__":
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    iceBreaker()
