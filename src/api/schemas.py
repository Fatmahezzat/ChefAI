from typing import Optional

from pydantic import BaseModel

class ModelRequest(BaseModel):
    prompt: str
    image: Optional[str] = None
    location: str
    thread_id: str = "1"

class ModelResponse(BaseModel):
    response: str
    thread_id: str = "1"