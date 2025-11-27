import { memo } from "react";
import { Message } from "../types";

interface Props {
  message: Message;
}

const roleStyles: Record<string, string> = {
  user: "bg-primary text-white self-end",
  assistant: "bg-slate-800 text-slate-100 self-start border border-slate-700",
  system: "bg-amber-100 text-amber-900 self-center",
};

export const ChatMessage = memo(({ message }: Props) => {
  const style = roleStyles[message.role] ?? roleStyles.assistant;
  return (
    <div className={`rounded-2xl px-4 py-3 max-w-2xl shadow ${style}`}>
      {message.content}
    </div>
  );
});
