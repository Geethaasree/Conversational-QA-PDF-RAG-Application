# RAG Q&A Conversation

A modular retrieval-augmented generation experience with a FastAPI backend and a modern React chat UI. Users upload PDFs, the backend indexes them with LangChain + Chroma using Groq + Hugging Face models, and the frontend offers a polished chat workflow.

## Repository Layout

```
backend/
  app/
    core/        # configuration & settings
    models/      # pydantic schemas for API traffic
    services/    # RAG orchestration logic
    main.py      # FastAPI app entrypoint
  requirements.txt
frontend/
  src/           # React + Tailwind chat interface
  package.json
```

Legacy `app.py` (Streamlit) is still present for reference, but the recommended path is the new backend/frontend pairing.

## Prerequisites

- Python 3.12+
- Node.js 18+
- Groq API key with chat permissions
- (Optional) Hugging Face token for embeddings (`HF_TOKEN`)

Create a `.env` in the repo root:

```
GROQ_API_KEY=sk_your_key
HF_TOKEN=hf_your_token
```

## Backend Setup

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Key endpoints:

- `POST /sessions/upload` — multipart form data (`files`) to start a session.
- `POST /sessions/{session_id}/chat` — JSON `{ "message": "..." }` to ask questions.
- `GET /health` — liveness probe.

The backend automatically maintains chat history per session in memory.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_BASE` in `frontend/.env` if the backend is not on `http://localhost:8000`.

## Workflow

1. Start the backend (uvicorn) and frontend (Vite dev server).
2. Visit `http://localhost:5173`.
3. Upload one or more PDFs via the drag-and-drop card.
4. Chat instantly with the indexed content; history persists per session until the backend restarts.

## Next Steps

- Add persistence (e.g., Postgres + pgvector) for cross-session memories.
- Secure the API with auth headers if deploying beyond localhost.
- Upgrade the frontend to support streaming responses.
