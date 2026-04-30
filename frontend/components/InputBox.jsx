"use client";

import { useState, useRef, useEffect } from "react";
import { Send, LifeBuoy, Sparkles } from "lucide-react";

const InputBox = ({ onSend, onRescue }) => {
  const [message, setMessage] = useState("");
  const [isSending, setIsSending] = useState(false);
  const textareaRef = useRef(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [message]);

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

  const charCount = message.length;
  const isMessageEmpty = !message.trim();

  return (
    <div className="relative group mt-6">
      {/* Decorative Glow */}
      <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500/20 to-indigo-500/20 rounded-[2.2rem] blur opacity-0 group-hover:opacity-100 transition duration-500"></div>
      
      <div className="relative rounded-[2rem] border border-slate-200/80 dark:border-slate-700 bg-white dark:bg-slate-900/80 backdrop-blur-md p-2 shadow-[0_8px_30px_rgb(0,0,0,0.04)] transition-all duration-300 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] hover:border-slate-300/80 dark:hover:border-slate-600">
        <div className="flex flex-col">
          {/* Input Area */}
          <div className="relative flex items-start">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Share your thoughts or ask a question..."
              className="w-full min-h-[60px] max-h-[200px] bg-transparent px-6 py-4 text-slate-800 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 outline-none resize-none text-[0.95rem] leading-relaxed"
            />
          </div>

          {/* Action Bar */}
          <div className="flex items-center justify-between px-4 pb-3 pt-2">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => onRescue?.()}
                className="flex items-center gap-2 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-xs font-bold text-slate-600 dark:text-slate-300 transition-all hover:bg-amber-50 dark:hover:bg-amber-900/20 hover:border-amber-200 dark:hover:border-amber-800 hover:text-amber-700 dark:hover:text-amber-400 active:scale-95 shadow-sm"
              >
                <LifeBuoy size={14} className="text-amber-500" />
                GET HINT
              </button>
              
              {charCount > 0 && (
                <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-md transition-all animate-in fade-in zoom-in duration-300">
                  {charCount} chars
                </span>
              )}
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={handleSend}
                disabled={isMessageEmpty || isSending}
                className={`
                  flex items-center gap-2 rounded-full px-6 py-2.5 text-sm font-bold transition-all duration-300 active:scale-95 shadow-lg
                  ${isMessageEmpty || isSending
                    ? "bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-600 cursor-not-allowed"
                    : "bg-slate-900 dark:bg-blue-600 text-white shadow-slate-200 dark:shadow-blue-900/20 hover:bg-slate-800 dark:hover:bg-blue-500 hover:-translate-y-0.5 hover:shadow-xl"}
                `}
              >
                {isSending ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-white" />
                ) : (
                  <Send size={16} className={isMessageEmpty ? "" : "animate-pulse"} />
                )}
                {isSending ? "SENDING" : "SEND MESSAGE"}
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Visual Indicator */}
      <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 flex items-center gap-1.5 opacity-40">
        <Sparkles size={10} className="text-blue-500" />
        <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 dark:text-slate-600">
          Curio AI Adaptive Engine Active
        </span>
      </div>
    </div>
  );
};

export default InputBox;
