import { FormEvent, useState } from "react";
import { Send } from "lucide-react";

interface Props {
  onSend(message: string): Promise<void> | void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: Props) {
  const [draft, setDraft] = useState("");

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!draft.trim() || disabled) {
      return;
    }
    const message = draft.trim();
    setDraft("");
    await onSend(message);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-3 bg-slate-900 rounded-3xl px-4 py-3 border border-slate-800"
    >
      <input
        className="flex-1 bg-transparent outline-none text-slate-100"
        placeholder="Ask anything about your PDFs..."
        value={draft}
        onChange={(event) => setDraft(event.target.value)}
        disabled={disabled}
      />
      <button
        type="submit"
        className="bg-primary rounded-full p-2 text-white disabled:opacity-40"
        disabled={disabled}
        aria-label="Send"
      >
        <Send className="h-5 w-5" />
      </button>
    </form>
  );
}
