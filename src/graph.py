"""Orchestration logic (arcs and nodes using LangGraph)"""
from langgraph.graph import START, END, StateGraph
from typing import Literal
from src.state import State
from langgraph.prebuilt import ToolNode, tools_condition
from src.tools.web_search import tavily_search
from src.agents.factory import AgentFactory


tools_node = ToolNode(tools=[tavily_search])

def decide_sufficient(state) -> Literal["researcher", "writer"]:
    return "researcher" if not state["is_sufficient"] else "writer"


class MultiAgentGraph:
    def __init__(self):
        self.builder = StateGraph(State)
        self.research_agent = AgentFactory.create("researcher")
        self.analyzer_agent = AgentFactory.create("analyzer")
        self.writer_agent = AgentFactory.create("writer")

        self.builder.add_node("researcher", self.research_agent.run) # this way LangGraph will call "run(state)" from the agent each time the flow reaches this node 
        self.builder.add_node("analyzer", self.analyzer_agent.run)
        self.builder.add_node("writer", self.writer_agent.run)
        self.builder.add_node("tools", tools_node)
        # Idea: 'researcher' search data using 'tool' which gives data back to the 
        #       'researcher' that appends it to the state and will then
        #       go to 'analyzer' which decides whether data is enough and if it 
        #       is goes to 'writer', otherwise it returns to 'researcher'
        self.builder.add_edge(START, "researcher")

        """Looks at the last message from the researcher, if called a tool 
        then goes to the tool node. Otherwise goes to the analyzer"""
        self.builder.add_conditional_edges(
            "researcher",
            tools_condition,
            {
                "tools": "tools",       #if condition uses tool, then go to node_tools 
                "__end__" : "analyzer"  #if condition ends, then go to analyzer
            }
        )

        self.builder.add_edge("tools", "researcher")
        self.builder.add_conditional_edges("analyzer", decide_sufficient)
        self.builder.add_edge("writer", END)
        self.graph = self.builder.compile()
 
 
    def run(self, input_state: State):
        return self.graph.invoke(input_state)
        