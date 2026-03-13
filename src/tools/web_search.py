from langchain_core.tools import tool
from tavily import TavilyClient
import os

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_KEY")) 

@tool
def tavily_search(query: str) -> list[dict]:
    """This function is used to retrieve information from the web following
    what is asked in the provided 'query' parameter"""
    response = tavily_client.search(query, include_images=True)
    return response["results"]