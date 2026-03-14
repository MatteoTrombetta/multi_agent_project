from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage
from src.graph import State
from src.tools import web_search

class ResearcherAgent:
    """Receives the query, decides which terms to search, uses 
    research tools and extract raw data and append them to State.
    It will use Tavily APIs"""
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) #temp=0 ideal for agents
        self.llm_with_tools = self.llm.bind_tools([web_search.tavily_search]) #binding the tool from the library

        self.agent_prompt = f"""You are an experienced researcher. 
        You have to search for academic data and information online, 
        based on the topics you are asked to search for"""

    def run(self, state: State) -> dict:
        # Giving context to the agent
        context = [SystemMessage(content=self.agent_prompt)] + state["chronology"]
        answer = self.llm_with_tools.invoke(context)
        return {"chronology": [answer]} # Remeber: by using [] you add the answer to the list!

