from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


class MySearchTool(BaseModel):
    query: str = Field(description="Should be a search query")


@tool("search_tool", args_schema=MySearchTool, return_direct=True)
def search(question: str) -> str:
    """simple tool to search"""
    return "langchain"


print(f"Detaisl of the tools are:{search.name} , {search.description}")
print(search.args)
