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

        self.agent_prompt = """You are an experienced researcher. 
        You must search for academic data and information online based on the user's query.
        CRITICAL INSTRUCTION: Before searching, ALWAYS read the conversation history. 
        If you see that an Analyzer has previously rejected your research, READ THEIR REASONING carefully. 
        DO NOT repeat the exact same search query. Formulate a NEW, more specific search query to find the exact missing information the Analyzer asked for."""

    def run(self, state: State) -> dict:
        # Giving context to the agent
        print("[Researcher] I'm looking for information...")
        context = [SystemMessage(content=self.agent_prompt)] + state["messages"]
        answer = self.llm_with_tools.invoke(context)
        return {"messages": [answer]} # Remeber: by using [] you add the answer to the list!

