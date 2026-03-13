from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from src.graph import search, State

class ResearcherAgent:
    """Receives the query, decides which terms to search, uses 
    research tools and extract raw data and append them to State.
    It will use Tavily APIs"""
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) #temp=0 ideal for agents
        self.llm_with_tools = self.llm.bind_tools([search]) #binding the tool from the library

        # optional
        self.agent_prompt = f"""You are an experienced researcher. 
        You have to search for academic data and information online, 
        based on the topics you are asked to search for"""

    def run(self, state: State) -> State:
        answer = self.llm_with_tools.invoke(state["chronology"])
        return {"chronology": [answer]} # Remeber: by using [] you add the answer to the list!



