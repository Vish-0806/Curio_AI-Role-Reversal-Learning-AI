"use client";

import { useState } from "react";
import { X, Lightbulb, BookOpen, RotateCcw } from "lucide-react";

const RescueHint = ({ isOpen, onClose, onApplyHint, currentTopic }) => {
  const [hintLevel, setHintLevel] = useState(1);
  const [showHint, setShowHint] = useState(false);

  const hints = {
    1: "Try breaking down the concept into smaller parts. What are the key components?",
    2: "Think about how this concept relates to things you already know.",
    3: "What would happen if you applied this concept in real life? Can you think of an example?",
  };

  const rescueOptions = [
    {
      id: "break_down",
      label: "Break It Down",
      icon: BookOpen,
      description: "Start with fundamentals",
    },
    {
      id: "example",
      label: "Give Example",
      icon: Lightbulb,
      description: "Show a real-world case",
    },
    {
      id: "reset",
      label: "Reset Approach",
      icon: RotateCcw,
      description: "Start explaining fresh",
    },
  ];

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="absolute inset-0 bg-slate-900/60 dark:bg-black/80 backdrop-blur-md animate-in fade-in duration-300"
      />

      {/* Modal Container */}
      <div className="relative w-full max-w-lg overflow-hidden rounded-[3rem] bg-white dark:bg-[#020617]/80 backdrop-blur-2xl shadow-[0_20px_50px_rgba(0,0,0,0.1)] dark:shadow-amber-900/20 animate-fade-in-up border border-slate-200 dark:border-white/10">
        {/* Decorative Top Bar */}
        <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-amber-400 to-amber-600"></div>

        <div className="relative p-10">
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute right-8 top-8 h-10 w-10 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:bg-rose-50 dark:hover:bg-rose-900/40 hover:text-rose-600 transition-all active:scale-95"
          >
            <X size={20} />
          </button>

          {/* Header */}
          <div className="mb-8 text-center">
            <div className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-[2rem] bg-amber-500 text-white shadow-xl shadow-amber-200 dark:shadow-amber-900/40 animate-float">
              <Lightbulb size={40} className="fill-current" />
            </div>
            <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tighter">
              Rescue <span className="text-amber-500">Mode</span>
            </h2>
            <p className="mt-2 text-sm font-medium text-slate-500 dark:text-slate-400">
              Don't worry! Let's approach this differently.
            </p>
          </div>

          {/* Hint Level Selector */}
          <div className="mb-8">
            <p className="mb-3 text-xs font-black uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500 text-center">
              Select Intervention Level
            </p>
            <div className="flex gap-3">
              {[1, 2, 3].map((level) => (
                <button
                  key={level}
                  onClick={() => {
                    setHintLevel(level);
                    setShowHint(true);
                  }}
                  className={`flex-1 rounded-[1.5rem] py-3 text-xs font-black transition-all duration-300 active:scale-95 border ${
                    hintLevel === level
                      ? "bg-amber-500 text-white border-amber-500 shadow-lg shadow-amber-500/30 scale-105"
                      : "bg-slate-50/50 dark:bg-white/5 border-slate-200 dark:border-white/10 text-slate-600 dark:text-slate-300 hover:border-amber-300 dark:hover:border-amber-500/50 hover:bg-amber-50 dark:hover:bg-amber-500/10"
                  }`}
                >
                  LEVEL {level}
                </button>
              ))}
            </div>
          </div>

          {/* Hint Display */}
          {showHint && (
            <div className="mb-8 rounded-[2rem] border border-amber-200 dark:border-amber-500/30 bg-amber-50/50 dark:bg-amber-500/5 backdrop-blur-md p-6 animate-fade-in-up">
              <div className="flex items-start gap-3">
                <Lightbulb size={20} className="text-amber-500 shrink-0 mt-0.5" />
                <p className="text-sm font-medium text-amber-900 dark:text-amber-200/90 leading-relaxed">
                  {hints[hintLevel]}
                </p>
              </div>
            </div>
          )}

          {/* Rescue Options */}
          <div className="space-y-3 mb-6">
            <div className="flex items-center gap-4 mb-4">
              <div className="flex-1 border-t border-slate-100 dark:border-slate-800"></div>
              <span className="text-[10px] font-black uppercase tracking-widest text-slate-300 dark:text-slate-700">
                Quick Actions
              </span>
              <div className="flex-1 border-t border-slate-100 dark:border-slate-800"></div>
            </div>

            {rescueOptions.map((option) => {
              const Icon = option.icon;
              return (
                <button
                  key={option.id}
                  onClick={() => {
                    onApplyHint(option.id);
                    onClose();
                  }}
                  className="group flex w-full items-center gap-4 rounded-[2rem] border border-slate-100 dark:border-white/5 bg-slate-50/50 dark:bg-white/5 backdrop-blur-md p-4 text-left transition-all hover:border-amber-300 dark:hover:border-amber-500/50 hover:bg-white dark:hover:bg-white/10 hover:shadow-xl hover:shadow-amber-100/20 dark:hover:shadow-amber-900/20 hover:-translate-y-1 active:scale-95"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-amber-100/50 dark:bg-amber-500/20 text-amber-600 transition-transform group-hover:scale-110">
                    <Icon size={18} />
                  </div>
                  <div>
                    <p className="font-black text-slate-900 dark:text-white text-sm">
                      {option.label}
                    </p>
                    <p className="text-[11px] font-bold text-slate-500 dark:text-slate-400">
                      {option.description}
                    </p>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Info */}
          <div className="mt-8 flex items-center justify-center gap-2">
            <BookOpen size={14} className="text-amber-500" />
            <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 dark:text-slate-500">
              Every attempt helps you learn
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RescueHint;

