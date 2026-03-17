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

        self.agent_prompt = """You are an experienced analyzer. 
        Your goal is to look at the data provided by the researcher and decide if it's enough to answer the user's query.
        CRITICAL INSTRUCTION: You don't need a perfectly comprehensive encyclopedia. If the provided data contains at least 3-4 solid, relevant facts or recent developments that can form a good short report, you MUST output is_sufficient = True. 
        Only output False if the data is completely irrelevant, completely empty, or completely misses the core of the user's question."""

    def run(self, state: State) -> dict:
        print("[Analyzer] I'm evaluating the data...")    
        context = [
            SystemMessage(self.agent_prompt),
            HumanMessage(content=f"Original query from the user: {state["initial_query"]}")
            ] + state["messages"]
        answer = self.structured_llm.invoke(context)
        
        return {
            "messages": [AIMessage(content=answer.reasoning)],
            "is_sufficient": answer.is_sufficient
        }
