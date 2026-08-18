import uuid

from fastapi import APIRouter
from langchain.messages import HumanMessage

from routers.ModelRouter import ModelResponse, ModelRequest
from src.agent.agent import AGENT
from src.utils.helpers import image_to_base64

router = APIRouter(prefix="/model", tags=["Model"])

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