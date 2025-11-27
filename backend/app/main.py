from __future__ import annotations

from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.models.schemas import ChatMessage, ChatRequest, ChatResponse, UploadResponse
from app.services.rag_service import RAGService

settings = get_settings()
rag_service = RAGService(settings)

app = FastAPI(title="RAG Q&A Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/sessions/upload", response_model=UploadResponse)
async def upload_pdfs(files: List[UploadFile] = File(...)) -> UploadResponse:
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload at least one PDF")

    pdf_payload = []
    for upload in files:
        if upload.content_type not in ("application/pdf", "application/octet-stream"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported")
        content = await upload.read()
        pdf_payload.append((upload.filename, content))
    try:
        session_id, doc_count = rag_service.create_session(pdf_payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return UploadResponse(session_id=session_id, documents=doc_count)


@app.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def chat_with_session(session_id: str, payload: ChatRequest) -> ChatResponse:
    try:
        answer, history = rag_service.ask(session_id, payload.message)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    messages = [
        ChatMessage(role=message.type, content=message.content)
        for message in history.messages
    ]
    return ChatResponse(answer=answer, history=messages)
