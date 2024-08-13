from langchain.schema import BaseOutputParser, StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict, Any


class Summary(BaseModel):
    summary: str = Field(description="summary")
    facts: List[str] = Field(description="Intersting factis about a person")

    def to_dic(self) -> Dict[str, Any]:
        return {"Summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
