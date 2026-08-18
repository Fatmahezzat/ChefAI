import os

from tavily import TavilyClient

from langchain.tools import tool

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_API_KEY:
    TAVILY_CLIENT = TavilyClient(api_key=TAVILY_API_KEY)
else:
    TAVILY_CLIENT = None

@tool
def find_nearby_supermarkets(location: str) -> str:
    """
    Find nearby supermarkets based on user's location.
    """

    result = TAVILY_CLIENT.search(
        query=f"Best supermarkets near {location}",
        search_depth="advanced",
        include_answer=True,
        max_results=5,
    )

    return result["answer"]