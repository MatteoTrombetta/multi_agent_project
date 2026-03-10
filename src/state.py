from typing import TypedDict, NotRequired, ReadOnly, Annotated
from src.tools.message import Message
from langgraph.graph import START, StateGraph
import operator

class State(TypedDict):
    """Class to define the structure of the State, uses TypedDict.
    Necessary to use Annotated class in order to avoid overwriting."""
    initial_query: str
    docs_found: Annotated[list[str], operator.add]
    raw_data: Annotated[list[object], operator.add]
    chronology: Annotated[list[Message], operator.add]
    something: NotRequired[str] #see if needs anything else
    final_report: dict #let's keep it simple
    research_steps: int # to keep a counting of the steps performed reasearching

