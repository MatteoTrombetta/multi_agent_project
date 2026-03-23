from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain_core.messages import SystemMessage
from src.graph import State
from src.tools.web_search import tavily_search
from src.tools.company_knowledge import search_company_knowledge

class ResearcherAgent:
    """Receives the query, decides which terms to search, uses 
    research tools and extract raw data and append them to State.
    It will use Tavily APIs or internal company rules: you have access 
    to two distinct tools. If the user asks about company policies, escalation,
    or internal rules, you MUST use the internal database tool. If the user asks 
    about external events, global news, or general knowledge, you MUST use the web
    search tool. If a complex query requires both, use them sequentially."""
    def __init__(self):
        self._llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) #temp=0 ideal for agents
        self._llm_with_tools = self._llm.bind_tools([tavily_search, search_company_knowledge]) #binding the tool from the library

        # Online Search behaviour
        self._agent_prompt = """You are an experienced researcher. 
        You must search for academic data and information online based on the user's query.
        You must use the provided tool to search the company internal database for policies. Do not invent answers.
        CRITICAL INSTRUCTION: Before searching, ALWAYS read the conversation history. 
        If you see that an Analyzer has previously rejected your research, READ THEIR REASONING carefully. 
        DO NOT repeat the exact same search query. Formulate a NEW, more specific search query to find the exact missing information the Analyzer asked for."""


    def run(self, state: State) -> dict:
        # Giving context to the agent
        print("[Researcher] I'm looking for information...")
        context = [SystemMessage(content=self._agent_prompt)] + state["messages"]
        answer = self._llm_with_tools.invoke(context)
        return {"messages": [answer]} #remeber: by using '[]' you add the answer to the list

