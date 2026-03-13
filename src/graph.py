"""Orchestration logic (arcs and nodes using LangGraph)"""
from langgraph.graph import START, END, StateGraph
from typing import Literal
from src.graph import State
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import AnyMessage
from src.agents.researcher import ResearcherAgent


@tool
def search(state): # dummy tool for checking whether APIs work
    """Function that through API calls search on the web and retrieves data"""
    messages = state["chronology"]
    return 

def analyze(state):
    return None

def write(state):
    return None

def call(state):
    return None

def decide_sufficient(state) -> Literal["researcher", "writer"]:
    return "researcher" if ... else "writer"

def decide_tool(runtime: ToolRuntime) -> Literal["tool", "analyzer"]:
    """Looks at the last message from the researcher, if called a tool 
    then goes to the tool node. Otherwise goes to the analyzer"""
    # dovrebbe essere una roba del genere
    #return "tool" if runtime.state["messages"][-1] == 'tool' else "analyzer"
    return


class MultiAgentGraph:
    def __init__(self):
        self.builder = StateGraph(State)
        self.research_agent = ResearcherAgent()

        self.builder.add_node("researcher", self.research_agent.run) # this way LangGraph will call "run(state)" from the agent each time the flow reach this node 
        self.builder.add_node("analyzer", analyze)
        self.builder.add_node("writer", write)
        self.builder.add_node("tool", call)
        # Idea: 'researcher' search data using 'tool' which gives data back to the 
        #       'researcher' that appends it to the state and will then
        #       go to 'analyzer' which decides whether data is enough and if it 
        #       is goes to 'writer', otherwise it returns to 'researcher'
        self.builder.add_edge(START, "researcher")
        self.builder.add_conditional_edges("researcher", decide_tool)
        self.builder.add_edge("tool", "researcher")
        self.builder.add_conditional_edges("analyzer", decide_sufficient)
        self.builder.add_edge("writer", END)
        self.graph = self.builder.compile()
        
    def run(self, input_state: State):
        return self.graph.invoke()
        