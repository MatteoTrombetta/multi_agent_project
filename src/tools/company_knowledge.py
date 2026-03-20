from langchain_core.tools import tool
from src.db_connection import VectorDBConnection


@tool
def search_company_knowledge(query: str):
    """Use this tool ONLY to search for internal company policies, 
    business process management guidelines, internal rules, and escalation procedures."""
    db_connection = VectorDBConnection()
    db = db_connection.get_db() #Get the singleton
    top_k = db.similarity_search(query=query, k=2)
    texts_found = [doc.page_content for doc in top_k]
    result = "\n\n".join(texts_found)
    return result