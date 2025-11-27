from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import Settings


@dataclass
class SessionState:
    retriever: Any
    history: ChatMessageHistory


class RAGService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        if settings.hf_token:
            os.environ.setdefault("HF_TOKEN", settings.hf_token)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.llm = ChatGroq(groq_api_key=settings.groq_api_key, model_name=settings.groq_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        self.contextualize_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        self.sessions: Dict[str, SessionState] = {}

    def _format_docs(self, docs) -> str:
        return "\n\n".join(doc.page_content for doc in docs) if docs else ""

    def _contextualize(self, question: str, history: Iterable) -> str:
        if not history:
            return question
        messages = self.contextualize_prompt.format_messages(
            chat_history=history,
            input=question,
        )
        response = self.llm.invoke(messages)
        return getattr(response, "content", response)

    def _answer(self, question: str, docs, history: Iterable) -> str:
        messages = self.qa_prompt.format_messages(
            chat_history=history,
            input=question,
            context=self._format_docs(docs),
        )
        response = self.llm.invoke(messages)
        return getattr(response, "content", response)

    def _load_documents(self, file_paths: List[Path]):
        documents = []
        for path in file_paths:
            loader = PyPDFLoader(str(path))
            documents.extend(loader.load())
        return documents

    def create_session(self, files: Sequence[Tuple[str, bytes]]) -> Tuple[str, int]:
        temp_paths: List[Path] = []
        for _, content in files:
            with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(content)
                temp_paths.append(Path(tmp.name))
        try:
            documents = self._load_documents(temp_paths)
        finally:
            for path in temp_paths:
                path.unlink(missing_ok=True)
        if not documents:
            raise ValueError("Uploaded PDFs contained no readable text")
        splits = self.text_splitter.split_documents(documents)
        if not splits:
            raise ValueError("Uploaded PDFs could not be chunked")
        collection_name = f"{self.settings.collection_name}-{uuid.uuid4()}"
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embeddings,
            collection_name=collection_name,
        )
        retriever = vectorstore.as_retriever()
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = SessionState(
            retriever=retriever,
            history=ChatMessageHistory(),
        )
        return session_id, len(documents)

    def _get_history(self, session_id: str) -> BaseChatMessageHistory:
        state = self.sessions.get(session_id)
        if not state:
            raise KeyError("Session not found")
        return state.history

    def ask(self, session_id: str, question: str) -> Tuple[str, ChatMessageHistory]:
        if session_id not in self.sessions:
            raise KeyError("Session not found")
        state = self.sessions[session_id]
        history = state.history
        standalone_question = self._contextualize(question, history.messages)
        docs = state.retriever.invoke(standalone_question)
        answer = self._answer(question, docs, history.messages)
        history.add_user_message(question)
        history.add_ai_message(answer)
        return answer, history
