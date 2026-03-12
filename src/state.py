from typing import TypedDict, NotRequired, ReadOnly, Annotated
from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph.message import add_messages #does not duplicates graph
import operator

#NB: Could be also implemented with a pydantic base model.
# pydantic is more suitable when you need to enforce data constraints

class State(TypedDict):
    """Class to define the structure of the State, uses TypedDict.
    Necessary to use Annotated class in order to avoid overwriting."""
    initial_query: str
    graph_state: str # don't know if this is needed
    docs_found: Annotated[list[str], operator.add]
    raw_data: Annotated[list[dict], operator.add] #will be with smth like 'url', 'content'
    chronology: Annotated[list[AnyMessage], add_messages]
    something: NotRequired[str] #see if needs anything else
    final_report: dict #let's keep it simple
    research_steps: Annotated[int, lambda x, y: x+y] # custom reducer (TO CHECK)
    research_steps_old: int # to keep a counting of the steps performed reasearching

    
'''
Node functions follow this pattern:
1.Receive current state as input
2.Process data using schema-appropriate access pattern
3.Return dictionary with keys to update
4.LangGraph merges returned values into state

The returned dictionary needs only the keys the node wants to modify - unchanged keys are preserved.
'''