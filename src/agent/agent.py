from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from src.models.llm_client import get_llm
from src.tools.search import web_search
from src.tools.supermarkets import find_nearby_supermarkets
from src.prompts.system_prompts import CHEFAI_SYSTEM_PROMPT

AGENT = create_agent(
        model = get_llm(),
        checkpointer = MemorySaver(),
        tools=[web_search, find_nearby_supermarkets],
        system_prompt = CHEFAI_SYSTEM_PROMPT
        )