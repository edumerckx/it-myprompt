from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ChatSchema(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    id: UUID
    user_id: UUID
    prompt: str
    response: str
    model: str
    created_at: datetime
