"use client";

import React, { useEffect, useRef } from "react";
import { Lightbulb, AlertCircle, CheckCircle2, HelpCircle, BookOpen } from "lucide-react";

const ChatWindow = ({ messages = [] }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const getMessageIcon = (intent) => {
    switch (intent) {
      case "hint":
        return <Lightbulb size={16} />;
      case "challenge":
        return <AlertCircle size={16} />;
      case "acknowledgment":
        return <CheckCircle2 size={16} />;
      case "question":
        return <HelpCircle size={16} />;
      case "student":
        return <BookOpen size={16} />;
      default:
        return null;
    }
  };

  const getIntentColor = (intent) => {
    switch (intent) {
      case "hint":
        return "border-amber-200 bg-amber-50 text-amber-900 dark:bg-amber-900/10 dark:border-amber-900/30 dark:text-amber-400";
      case "challenge":
        return "border-rose-200 bg-rose-50 text-rose-900 dark:bg-rose-900/10 dark:border-rose-900/30 dark:text-rose-400";
      case "acknowledgment":
        return "border-emerald-200 bg-emerald-50 text-emerald-900 dark:bg-emerald-900/10 dark:border-emerald-900/30 dark:text-emerald-400";
      case "question":
      case "student":
        return "border-blue-200 bg-blue-50 text-blue-900 dark:bg-blue-900/10 dark:border-blue-900/30 dark:text-blue-400";
      default:
        return "border-slate-200 bg-slate-50 text-slate-900 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-300";
    }
  };

  return (
    <div className="flex h-[500px] flex-col rounded-3xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm overflow-hidden">
      {/* Messages Container */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto space-y-6 p-4 px-6 py-6"
      >
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center text-center">
            <div className="animate-fade-in-up">
              <div className="mx-auto w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center text-white mb-4 shadow-xl shadow-blue-200 dark:shadow-blue-900/20">
                <BookOpen size={32} />
              </div>
              <p className="text-2xl font-black text-slate-900 dark:text-white tracking-tighter">👋 Hello Teacher!</p>
              <p className="mt-2 text-slate-500 dark:text-slate-400 font-medium">
                I'm Curio, your curious student. <br />
                Start by explaining a topic!
              </p>
            </div>
          </div>
        ) : (
          messages.map((message, index) => {
            const isUser = message.role === "user";
            const intent = message.ai_intent || "question";

            return (
              <div
                key={index}
                className={`flex ${isUser ? "justify-end" : "justify-start"} animate-fade-in-up`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div
                  className={`max-w-[85%] space-y-2 ${
                    isUser ? "items-end" : "items-start"
                  }`}
                >
                  {/* Role label */}
                  <div className={`flex items-center gap-2 mb-1 ${isUser ? "flex-row-reverse" : ""}`}>
                    <p className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 dark:text-slate-600">
                      {isUser ? "You (Teacher)" : `Curio (${intent})`}
                    </p>
                    <div className={`h-1 w-1 rounded-full ${isUser ? "bg-blue-600" : "bg-slate-300 dark:bg-slate-700"}`}></div>
                  </div>

                  {/* Message bubble */}
                  <div
                    className={`rounded-2xl px-5 py-4 shadow-sm transition-all hover:shadow-md ${
                      isUser
                        ? "rounded-tr-lg bg-blue-600 text-white font-medium"
                        : `rounded-tl-lg border ${getIntentColor(intent)}`
                    }`}
                  >
                    <p className="whitespace-pre-wrap break-words text-[0.95rem] leading-relaxed">
                      {message.content || message.ai_message}
                    </p>

                    {/* Intent indicator for AI messages */}
                    {!isUser && intent && (
                      <div className="mt-3 pt-3 border-t border-current opacity-20 flex items-center gap-2 text-[10px] font-black uppercase tracking-widest">
                        {getMessageIcon(intent)}
                        <span>{intent} Intent</span>
                      </div>
                    )}
                  </div>

                  {/* Followups */}
                  {!isUser && message.followups && message.followups.length > 0 && (
                    <div className="mt-3 space-y-2 pl-2">
                      {message.followups.map((followup, idx) => (
                        <div key={idx} className="flex items-center gap-2 group cursor-pointer">
                          <div className="h-1.5 w-1.5 rounded-full bg-blue-400/50 group-hover:bg-blue-500 transition-colors"></div>
                          <p className="text-[11px] font-bold text-slate-500 dark:text-slate-500 hover:text-blue-600 transition-colors italic">
                            {followup}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Footer indicator */}
      <div className="border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 px-6 py-3 flex justify-between items-center">
        <div className="flex gap-1">
          {[0, 1, 2].map(i => <div key={i} className="h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-700"></div>)}
        </div>
        <p className="text-[10px] font-black uppercase tracking-widest text-slate-400 dark:text-slate-600">
          {messages.length} Interaction{messages.length === 1 ? "" : "s"}
        </p>
      </div>
    </div>
  );
};

export default ChatWindow;
