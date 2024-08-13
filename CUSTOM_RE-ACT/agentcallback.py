from langchain.callbacks.base import BaseCallbackHandler
from typing import Dict, List, Optional, Any
from langchain_core.outputs import LLMResult
from uuid import UUID


class AgentCallBackHandler(BaseCallbackHandler):
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM is starting"""
        print(f"prompt at the begining is ***\n {prompts[0]}")
        print("***************")

    def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when llm has finished executing"""
        print(f"LLM response  is ***\n {response.generations[0][0].text}")
        print("***************")
