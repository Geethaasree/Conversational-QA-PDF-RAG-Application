import axios from "axios";
import { useMemo, useState } from "react";
import { Brain, Loader2 } from "lucide-react";

import { ChatInput } from "./components/ChatInput";
import { ChatMessage } from "./components/ChatMessage";
import { UploadZone } from "./components/UploadZone";
import { Message } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

function toMessageId(prefix: string) {
  return `${prefix}-${crypto.randomUUID()}`;
}

function normalizeHistory(raw: { role: string; content: string }[]): Message[] {
  return raw.map((item) => ({
    id: toMessageId(item.role),
    role: item.role === "human" ? "user" : item.role === "ai" ? "assistant" : (item.role as Message["role"]),
    content: item.content,
  }));
}

function App() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [uploading, setUploading] = useState(false);
  const [sending, setSending] = useState(false);
  const [status, setStatus] = useState("Upload PDFs to start chatting.");
  const [error, setError] = useState<string | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);

  const canChat = useMemo(() => Boolean(sessionId) && !uploading, [sessionId, uploading]);

  const handleUpload = async (files: FileList) => {
    const selectedFiles = Array.from(files);
    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append("files", file));
    setUploadedFiles(selectedFiles.map((file) => file.name));
    setUploading(true);
    setError(null);
    setStatus("Indexing your documents...");
    try {
      const { data } = await axios.post(`${API_BASE}/sessions/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSessionId(data.session_id);
      setMessages([]);
      setStatus(`Ready! Indexed ${data.documents} documents. Ask away.`);
    } catch (err: unknown) {
      setError("Upload failed. Please try again.");
      console.error(err);
      setUploadedFiles([]);
    } finally {
      setUploading(false);
    }
  };

  const handleSend = async (message: string) => {
    if (!sessionId) {
      setError("Upload PDFs first to start a session.");
      return;
    }
    setSending(true);
    setError(null);
    const optimistic: Message = { id: toMessageId("user"), role: "user", content: message };
    setMessages((prev) => [...prev, optimistic]);
    try {
      const { data } = await axios.post(`${API_BASE}/sessions/${sessionId}/chat`, { message });
      setMessages(normalizeHistory(data.history));
      setStatus("Answer ready. Ask another question!");
    } catch (err: unknown) {
      setError("Could not fetch answer. Check backend logs.");
      console.error(err);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white">
      <div className="max-w-6xl mx-auto px-6 py-10 flex flex-col gap-8">
        <header className="flex flex-col gap-2">
          <div className="flex items-center gap-3 text-2xl font-semibold">
            <Brain className="text-primary" />
            Conversational PDF QA
          </div>
          <p className="text-slate-400 max-w-3xl">
            Upload one or more PDF documents and chat with them instantly. Your Groq API key stays on the server; the UI is a clean chat-first experience.
          </p>
        </header>

        <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <UploadZone onSelect={handleUpload} disabled={uploading} />
            <div className="mt-4 text-sm text-slate-400 bg-slate-900 rounded-3xl px-4 py-3 border border-slate-800">
              <p className="font-semibold text-slate-200">Status</p>
              <p>{status}</p>
              {uploadedFiles.length > 0 && (
                <div className="mt-3 text-slate-300">
                  <p className="text-xs uppercase tracking-wide text-slate-500">Files</p>
                  <ul className="mt-1 space-y-1 text-sm">
                    {uploadedFiles.map((file) => (
                      <li key={file} className="truncate" title={file}>
                        {file}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {error && <p className="text-rose-400 mt-2">{error}</p>}
            </div>
          </div>

          <div className="lg:col-span-2 flex flex-col bg-slate-900/70 border border-slate-800 rounded-3xl p-6 min-h-[600px]">
            <div className="flex-1 overflow-y-auto flex flex-col gap-4 pr-2">
              {messages.length === 0 ? (
                <div className="text-center text-slate-500 mt-24">
                  <p className="text-lg font-semibold mb-2">No messages yet</p>
                  <p>Upload PDFs and ask your first question to begin.</p>
                </div>
              ) : (
                messages.map((message) => <ChatMessage key={message.id} message={message} />)
              )}
            </div>
            <div className="mt-6">
              <ChatInput onSend={handleSend} disabled={!canChat || sending} />
              {sending && (
                <div className="flex items-center gap-2 text-sm text-slate-400 mt-2">
                  <Loader2 className="h-4 w-4 animate-spin" /> Generating answer...
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
