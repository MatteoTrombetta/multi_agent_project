from langgraph.graph import START, END, StateGraph
from typing import Literal
from src.state import State
from langgraph.prebuilt import ToolNode, tools_condition
from src.tools.web_search import tavily_search
from src.agents.factory import AgentFactory
from src.tools.company_knowledge import search_company_knowledge
from langgraph.checkpoint.memory import MemorySaver

my_tools = [tavily_search, search_company_knowledge] # tools to search online & into company knowledge database for policies
tools_node = ToolNode(tools=my_tools)

#reflection loop
def decide_sufficient(state) -> Literal["researcher", "writer"]:
    return "researcher" if not state["is_sufficient"] else "writer"


class MultiAgentGraph:
    def __init__(self):
        self.builder = StateGraph(State)

        #separating graph logic from agents
        self.research_agent = AgentFactory.create("researcher")
        self.analyzer_agent = AgentFactory.create("analyzer")
        self.writer_agent = AgentFactory.create("writer")
        self.memory = MemorySaver() #checkpointer to store checkpoints in memory

        self.builder.add_node("researcher", self.research_agent.run) # this way LangGraph will call "run(state)" from the agent each time the flow reaches this node 
        self.builder.add_node("analyzer", self.analyzer_agent.run)
        self.builder.add_node("writer", self.writer_agent.run)
        self.builder.add_node("tools", tools_node)

        #Orchestration Logic
        self.builder.add_edge(START, "researcher")

        #Looks at the last message from the researcher, if called a tool then goes to the tool node.
        #Otherwise goes to the analyzer.
        self.builder.add_conditional_edges(
            "researcher",
            tools_condition, #checks last message generated from the model
            {
                "tools": "tools",       #if condition uses tool, then go to node_tools 
                "__end__" : "analyzer"  #if condition ends, then go to analyzer
            }
        )
        self.builder.add_edge("tools", "researcher")
        self.builder.add_conditional_edges("analyzer", decide_sufficient) #reflection
        self.builder.add_edge("writer", END)
        #using memory and interrupt_before to implement human-in-the-loop
        self.graph = self.builder.compile(checkpointer=self.memory, interrupt_before=["writer"])
 
    #launch the first node (researcher), given the intial state with the user query
    def run(self, input_state: State, config: dict = None): #config contains the thread_id
        return self.graph.invoke(input_state, config=config)
        