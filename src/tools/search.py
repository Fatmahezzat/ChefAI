import os

from tavily import TavilyClient

from langchain.tools import tool

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_API_KEY:
    TAVILY_CLIENT = TavilyClient(api_key=TAVILY_API_KEY)
else:
    TAVILY_CLIENT = None

@tool
def web_search(query: str) -> str:
    """
    Search the web using Tavily and return relevant information.
    """
    tavily_response = TAVILY_CLIENT.search(
        search_depth = "basic",
        country = "Egypt",
        query = query
        )

    return tavily_response["answer"]