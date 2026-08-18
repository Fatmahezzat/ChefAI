import os
import uuid
import base64
from typing import Optional

from dotenv import load_dotenv
from fastapi import APIRouter
from httpx import Client
from pydantic import BaseModel
from tavily import TavilyClient

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

router = APIRouter(prefix="/model", tags=["Model"])

MODEL_NAME = "gemini-3.6-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

HTTP_CLIENT = Client()

if TAVILY_API_KEY:
    TAVILY_CLIENT = TavilyClient(api_key=TAVILY_API_KEY)
else:
    TAVILY_CLIENT = None 

class ModelRequest(BaseModel):
    prompt: str
    image: Optional[str] = None
    location: str
    thread_id: str = "1"

class ModelResponse(BaseModel):
    response: str
    thread_id: str = "1"

def image_to_base64(image_path: Optional[str]) -> Optional[str]:
    if not image_path:
        return None

    if not os.path.exists(image_path):
        return image_path

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

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

llm_model = init_chat_model(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        model_provider="google_genai",
        max_tokens=2000, 
        temperature=0.8,
        timeout=30.0,
        max_iterations=3,
        http_client=HTTP_CLIENT
    )
AGENT = create_agent(
        model = llm_model,
        checkpointer = MemorySaver(),
        tools=[web_search, find_nearby_supermarkets],
        system_prompt = """
            You are ChefAI, an expert chef, nutrition advisor, and grocery shopping assistant.

            Your responsibilities are:

            1. Food Recognition
            - If the user sends an image of a dish, analyze it carefully.
            - Identify the dish if possible.
            - Extract the most likely ingredients.
            - If you are not completely certain, clearly mention which ingredients are assumptions.

            2. Recipe Assistance
            - Explain how to prepare the dish.
            - Suggest ingredient substitutions when appropriate.
            - Estimate cooking time and difficulty.

            3. Healthy Alternatives
            - Always suggest healthier alternatives for the recipe when possible.
            - Recommend healthier cooking methods.
            - Suggest ingredient replacements that reduce calories, fat, sugar, or sodium while preserving the flavor.
            - Mention vegetarian, vegan, gluten-free, or high-protein alternatives when relevant.

            4. Grocery Shopping
            - If the user asks where to buy the ingredients, recommend nearby supermarkets based on the user's current location.
            - If the user's location is unknown, politely ask them to share their location (city, area, or GPS coordinates) before recommending stores.
            - Once the location is provided, use the available search tool to find nearby supermarkets and recommend suitable places.

            5. Web Search
            Use the web search tool whenever you need:
            - current supermarket information
            - store availability
            - opening hours
            - current prices
            - local grocery stores
            - recent information
            - information that may have changed

            Do not use web search for general cooking knowledge.

            6. Communication Style
            - Be friendly and professional.
            - Keep responses clear and organized.
            - Use bullet points when listing ingredients or stores.
            - Never invent information when you are uncertain.
            - Ask follow-up questions whenever additional information is required.
            """
)

@router.post("/chat", response_model=ModelResponse)
def chat_request(request: ModelRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    image = image_to_base64(request.image)
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("========== CHAT START ==========")
    print("thread_id:", thread_id)
    print("location:", request.location)
    print("has_image:", request.image is not None)

    if image:
        print("image length:", len(image))

    print("Calling AGENT...")

    content = [
    {
        "type": "text",
        "text": request.prompt,
    }
    ]

    if image:
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/webp;base64,{image}"
                },
            }
        )

    response = AGENT.invoke(
        {
            "messages": [
                HumanMessage(
                        content=content
                    )
            ]
        },
        config=config
    )

    print("AGENT RESPONSE RECEIVED")
    print(response)
    print("========== CHAT END ==========")

    assistant_message = response["messages"][-1]

    response_text = assistant_message.content[0]["text"] \
        if isinstance(assistant_message.content, list) \
        else assistant_message.content

    return ModelResponse(
        response=response_text,
        thread_id=thread_id
    )