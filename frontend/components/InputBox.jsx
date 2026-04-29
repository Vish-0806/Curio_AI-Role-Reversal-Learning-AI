"use client";

import { useState } from "react";
import { Send, LifeBuoy } from "lucide-react";

const InputBox = ({ onSend, onRescue }) => {
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleSend = async () => {
    const trimmed = message.trim();
    if (!trimmed || isSending) return;

    setIsSending(true);
    try {
      await onSend?.(trimmed);
      setMessage("");
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-3 shadow-sm transition hover:border-slate-300">
      <div className="flex flex-col gap-3">
        {/* Input Area */}
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Explain your understanding... (Shift+Enter for new line)"
          className="min-h-[80px] max-h-[160px] w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition placeholder-slate-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 resize-none"
        />

        {/* Action Buttons */}
        <div className="flex gap-2">
          <button
            type="button"
            onClick={() => onRescue?.()}
            className="flex items-center gap-2 rounded-xl border border-amber-300 bg-amber-50 px-4 py-2 text-sm font-semibold text-amber-700 transition hover:bg-amber-100"
          >
            <LifeBuoy size={16} />
            Rescue
          </button>

          <div className="flex-1"></div>

          <button
            type="button"
            onClick={handleSend}
            disabled={!message.trim() || isSending}
            className="flex items-center gap-2 rounded-xl bg-blue-600 px-6 py-2 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={16} />
            {isSending ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default InputBox;
