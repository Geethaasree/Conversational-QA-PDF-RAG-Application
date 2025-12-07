from typing import List

from pydantic import BaseModel


class UploadResponse(BaseModel):
    session_id: str
    documents: int


class ChatRequest(BaseModel):
    message: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    answer: str
    history: List[ChatMessage]
