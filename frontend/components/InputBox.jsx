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
      <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500/30 to-indigo-500/30 rounded-[2.7rem] blur-md opacity-0 group-hover:opacity-100 transition duration-500 pointer-events-none"></div>
      
      <div className="relative rounded-[2.5rem] border border-slate-200/80 dark:border-white/10 bg-white dark:bg-[#020617]/60 backdrop-blur-md p-2 shadow-[0_8px_30px_rgb(0,0,0,0.04)] transition-all duration-300 hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] hover:border-slate-300/80 dark:hover:border-white/20">
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
                className="flex items-center gap-2 rounded-2xl border border-slate-200 dark:border-white/10 bg-white dark:bg-white/5 backdrop-blur-md px-5 py-2.5 text-xs font-black tracking-widest text-slate-600 dark:text-white transition-all hover:bg-amber-50 dark:hover:bg-amber-500/20 hover:border-amber-200 dark:hover:border-amber-500/50 hover:text-amber-700 dark:hover:text-amber-400 active:scale-95 shadow-sm"
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
                  flex items-center gap-2 rounded-[2.5rem] px-8 py-3 text-sm font-black tracking-tighter transition-all duration-300 active:scale-95 shadow-lg
                  ${isMessageEmpty || isSending
                    ? "bg-slate-100 dark:bg-slate-800/50 text-slate-400 dark:text-slate-600 cursor-not-allowed border dark:border-white/5"
                    : "bg-slate-900 dark:bg-blue-600 text-white shadow-slate-900/20 dark:shadow-blue-600/30 hover:bg-slate-800 dark:hover:bg-blue-500 hover:scale-105 hover:shadow-xl"}
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
