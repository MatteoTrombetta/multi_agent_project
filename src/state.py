from typing import TypedDict, Annotated #to use reducers to add context to the metadata 
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages #does not duplicates graph
import operator

class State(TypedDict):
    """Class to define the structure of the State, uses TypedDict.
    Necessary to use class Annotated in order to avoid overwriting."""
    initial_query: str
    docs_found: Annotated[list[str], operator.add] #operator.add to concatenate and not substitute data
    raw_data: Annotated[list[dict], operator.add] #will be with smth like 'url', 'content'
    messages: Annotated[list[AnyMessage], add_messages] #contains the chrnology of the conversations, add.messages both control and appends
    final_report: str #to keep it simple 
    research_steps: Annotated[int, lambda x, y: x+y] # custom reducer, could be used in case the researcher takes too many steps
    is_sufficient: bool = False #to say whether new researches are needed
    
