from langchain_core.tools import tool
from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) 

@tool
def tavily_search(query: str) -> list[dict]:
    """Use this tool ONLY to search the public internet for world news, 
    general knowledge, recent developments, or external facts. 
    DO NOT use this for internal company rules."""
    response = tavily_client.search(query, include_images=True)
    return response["results"]