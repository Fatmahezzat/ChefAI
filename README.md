ChefAI

ChefAI is an AI-powered cooking assistant that helps users recognize dishes, understand ingredients, get recipe recommendations, find healthier alternatives, search the web for up-to-date information, and locate nearby supermarkets.

Features:

1. Food Recognition

    Analyze food images.

    Identify dishes and possible ingredients.

2. Recipe Assistance

    Provide cooking instructions.

    Suggest ingredient substitutions.

    Estimate cooking time and difficulty.

3. Healthy Alternatives

    Suggest healthier ingredients.

    Recommend healthier cooking methods.

    Suggest vegetarian, vegan, gluten-free, or high-protein alternatives when relevant.

4. Web Search

    Search the web for current information such as supermarket availability, opening hours, prices, and local grocery stores.

5. Nearby Supermarkets

    Find suitable supermarkets based on the user's location.

6. Conversation Memory

    Maintain conversations using a thread_id.

7. Image Input

    Accept food images through the chat API for dish analysis.

Technologies:

Python

FastAPI

LangChain

LangGraph

Google Gemini

Tavily

HTML / CSS / JavaScript

Installation:

1. Clone the repository

git clone <your-repository-url>
cd ChefAI

2. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root:

GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key

Running the Application

Start the FastAPI server:

uvicorn main:app --reload

The application will be available at:

http://127.0.0.1:8000

FastAPI interactive documentation:

http://127.0.0.1:8000/docs

If the frontend is served by FastAPI, open:

http://127.0.0.1:8000

API:

Chat

Endpoint:

POST /model/chat

The endpoint accepts a text prompt and can optionally receive an image, location, and conversation thread ID.

Example Request

{
  "prompt": "Give me a healthy recipe using chicken",
  "image": null,
  "location": "Cairo, Egypt",
  "thread_id": "1"
}

Example Response

{
  "response": "Here is a healthy chicken recipe...",
  "thread_id": "1"
}

Frontend Request

The frontend communicates with the backend using:

fetch("/model/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    prompt: message,
    image: null,
    location: location,
    thread_id: threadId
  })
});

Using /model/chat instead of a hard-coded host allows the frontend and backend to run from the same FastAPI server.

Architecture:

ChefAI follows a modular AI-agent architecture:

                         ┌──────────────┐
                         │    User      │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   Frontend   │
                         │ HTML/CSS/JS  │
                         └──────┬───────┘
                                │
                                │ POST /model/chat
                                ▼
                         ┌──────────────┐
                         │   FastAPI    │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  API Routes  │
                         │   /api       │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  AI Agent    │
                         └──────┬───────┘
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
             ┌───────┐     ┌────────┐    ┌─────────────┐
             │ Gemini│     │ Tavily │    │ Supermarket │
             │  LLM  │     │ Search │    │    Tool     │
             └───────┘     └────────┘    └─────────────┘

Responsibilities

Frontend → User interface and communication with the API.

API → Handles HTTP requests, validation, and responses.

Agent → Controls AI reasoning, conversation memory, and tool usage.

Models → Configures the LLM.

Tools → Provides external capabilities such as web search and supermarket search.

Prompts → Contains system and agent instructions.

Utils → Contains reusable helper functions.

Tests → Contains unit and integration tests.

Future Improvements:

    Extending the agent to support MCP-based tool integration for standardized access to external tools and services.

    Add persistent conversation storage.

    Improve food image recognition.

    Add nutrition information.

    Recommend recipes based on available ingredients.

    Support more grocery stores and locations.

    Improve frontend UI/UX.

    Add authentication and user profiles.

    Add more specialized cooking tools.

Author

Fatmah Ezzat