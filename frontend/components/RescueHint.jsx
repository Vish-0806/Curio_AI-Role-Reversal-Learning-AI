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
    <div className="fixed inset-0 z-40 flex items-end justify-center bg-black/20 backdrop-blur-sm sm:items-center">
      <div className="relative w-full max-w-md rounded-t-3xl bg-white p-6 shadow-2xl sm:rounded-3xl">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute right-4 top-4 text-slate-400 hover:text-slate-600"
        >
          <X size={24} />
        </button>

        {/* Header */}
        <div className="mb-6 pr-8">
          <div className="mb-2 flex items-center gap-2">
            <Lightbulb size={24} className="text-amber-600" />
            <h2 className="text-2xl font-bold text-slate-900">Rescue Mode</h2>
          </div>
          <p className="text-sm text-slate-600">
            Don't worry! Let's approach this differently.
          </p>
        </div>

        {/* Hint Level Selector */}
        <div className="mb-6">
          <p className="mb-3 text-sm font-semibold text-slate-700">Hint Level</p>
          <div className="flex gap-2">
            {[1, 2, 3].map((level) => (
              <button
                key={level}
                onClick={() => {
                  setHintLevel(level);
                  setShowHint(true);
                }}
                className={`flex-1 rounded-lg px-3 py-2 text-sm font-semibold transition ${
                  hintLevel === level
                    ? "bg-amber-600 text-white"
                    : "border border-slate-200 bg-slate-50 text-slate-900 hover:border-amber-300"
                }`}
              >
                Level {level}
              </button>
            ))}
          </div>
        </div>

        {/* Hint Display */}
        {showHint && (
          <div className="mb-6 rounded-2xl border-l-4 border-amber-400 bg-amber-50 p-4">
            <p className="text-sm text-amber-900">{hints[hintLevel]}</p>
          </div>
        )}

        {/* Rescue Options */}
        <div className="mb-6 space-y-2">
          <p className="text-sm font-semibold text-slate-700">Quick Actions</p>
          {rescueOptions.map((option) => {
            const Icon = option.icon;
            return (
              <button
                key={option.id}
                onClick={() => {
                  onApplyHint(option.id);
                  onClose();
                }}
                className="flex w-full items-start gap-3 rounded-2xl border border-slate-200 p-3 text-left transition hover:border-amber-400 hover:bg-amber-50"
              >
                <Icon size={20} className="mt-0.5 flex-shrink-0 text-amber-600" />
                <div>
                  <p className="font-semibold text-slate-900">{option.label}</p>
                  <p className="text-xs text-slate-600">{option.description}</p>
                </div>
              </button>
            );
          })}
        </div>

        {/* Info */}
        <p className="text-center text-xs text-slate-500">
          You're doing great! Every attempt helps you learn.
        </p>
      </div>
    </div>
  );
};

export default RescueHint;
