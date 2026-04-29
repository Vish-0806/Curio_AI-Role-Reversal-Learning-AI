"use client";

import React, { useEffect, useRef } from "react";
import { Lightbulb, AlertCircle, CheckCircle2, HelpCircle } from "lucide-react";

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
      default:
        return null;
    }
  };

  const getIntentColor = (intent) => {
    switch (intent) {
      case "hint":
        return "border-amber-200 bg-amber-50";
      case "challenge":
        return "border-red-200 bg-red-50";
      case "acknowledgment":
        return "border-green-200 bg-green-50";
      case "question":
        return "border-blue-200 bg-blue-50";
      default:
        return "border-slate-200 bg-slate-50";
    }
  };

  return (
    <div className="flex h-[500px] flex-col rounded-3xl border border-slate-200 bg-white shadow-sm">
      {/* Messages Container */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto space-y-4 p-4 px-6 py-5"
      >
        {messages.length === 0 ? (
          <div className="flex h-full items-center justify-center text-center">
            <div>
              <p className="text-2xl font-semibold text-slate-900">👋 Hello!</p>
              <p className="mt-2 text-slate-500">
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
                className={`flex ${isUser ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] space-y-1 ${
                    isUser ? "items-end" : "items-start"
                  }`}
                >
                  {/* Role label */}
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                    {isUser ? "You (Teacher)" : `Curio (${intent})`}
                  </p>

                  {/* Message bubble */}
                  <div
                    className={`rounded-2xl px-4 py-3 shadow-sm ${
                      isUser
                        ? "rounded-tr-lg bg-blue-600 text-white"
                        : `rounded-tl-lg border ${getIntentColor(intent)} text-slate-900`
                    }`}
                  >
                    <p className="whitespace-pre-wrap break-words text-sm leading-6">
                      {message.content || message.ai_message}
                    </p>

                    {/* Intent indicator for AI messages */}
                    {!isUser && intent && (
                      <div className="mt-2 flex items-center gap-1 text-xs opacity-70">
                        {getMessageIcon(intent)}
                        <span className="capitalize">{intent}</span>
                      </div>
                    )}
                  </div>

                  {/* Followups */}
                  {!isUser && message.followups && message.followups.length > 0 && (
                    <div className="mt-2 space-y-2">
                      {message.followups.map((followup, idx) => (
                        <p
                          key={idx}
                          className="text-xs italic text-slate-500"
                        >
                          💡 {followup}
                        </p>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Message count indicator */}
      <div className="border-t border-slate-100 px-6 py-2 text-right">
        <p className="text-xs text-slate-400">
          {messages.length} {messages.length === 1 ? "message" : "messages"}
        </p>
      </div>
    </div>
  );
};

export default ChatWindow;

