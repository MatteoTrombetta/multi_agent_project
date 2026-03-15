from langchain_openai import ChatOpenAI
from src.state import State
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

class LLMResponse(BaseModel):
    """Response structure for the LLM"""
    reasoning: str = Field(description="The reasoning behind deciding whether the provided information is enough to answer the query")
    is_sufficient: bool = Field(description="Whether the provided information is sufficient (True) or not (False)")

class AnalyzerAgent:
    """Reads raw data from State. If they are enough, he 
    will extract key insights. If not enough he will send
    back the execution to the reasercher (keeping the cycle going)"""
    def __init__(self):

        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.structured_llm = self.llm.with_structured_output(LLMResponse)

        self.agent_prompt = f"""You are an experienced analyzer. 
        Your goal is to look at the data you received from the researcher
        and query from the user to understand whether the information
        is enough to answer to the user's query."""

    def run(self, state: State) -> dict:

        context = [
            SystemMessage(self.agent_prompt),
            HumanMessage(content=f"Original query from the user: {state["initial_query"]}")
            ] + state["chronology"]
        answer = self.structured_llm.invoke(context)
        
        return {
            "chronology": [AIMessage(content=answer.reasoning)],
            "is_sufficient": answer.is_sufficient
        }
