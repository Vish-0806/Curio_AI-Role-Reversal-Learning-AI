"use client";

import { useState, useEffect } from "react";
import { X, Zap, Sparkles, BookOpen, Search } from "lucide-react";

const TopicSelector = ({ onSelectTopic, isOpen }) => {
  const [customTopic, setCustomTopic] = useState("");

  useEffect(() => {
    if (isOpen) {
      setCustomTopic("");
    }
  }, [isOpen]);

  const presetTopics = [
    { id: "ohms_law", label: "Ohm's Law", icon: "⚡", color: "text-amber-500", bg: "bg-amber-50" },
    { id: "photosynthesis", label: "Photosynthesis", icon: "🌱", color: "text-emerald-500", bg: "bg-emerald-50" },
    { id: "water_cycle", label: "Water Cycle", icon: "💧", color: "text-blue-500", bg: "bg-blue-50" },
    { id: "gravity", label: "Gravity", icon: "🌍", color: "text-indigo-500", bg: "bg-indigo-50" },
    { id: "evolution", label: "Evolution", icon: "🧬", color: "text-rose-500", bg: "bg-rose-50" },
    { id: "calculus", label: "Calculus", icon: "∫", color: "text-purple-500", bg: "bg-purple-50" },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (customTopic.trim()) {
      onSelectTopic(customTopic.trim());
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        onClick={() => window.location.reload()}
        className="absolute inset-0 bg-slate-900/60 dark:bg-black/80 backdrop-blur-md animate-in fade-in duration-300"
      />

      {/* Modal Container */}
      <div className="relative w-full max-w-2xl overflow-hidden rounded-[3rem] bg-white dark:bg-slate-900 shadow-2xl animate-fade-in-up border border-slate-200 dark:border-slate-800">
        {/* Decorative Background */}
        <div className="absolute top-0 left-0 right-0 h-40 bg-gradient-to-b from-blue-600 to-indigo-600 opacity-5 dark:opacity-10"></div>
        
        <div className="relative p-10">
          {/* Close Button */}
          <button
            onClick={() => window.location.reload()}
            className="absolute right-8 top-8 h-10 w-10 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:bg-rose-50 dark:hover:bg-rose-900/40 hover:text-rose-600 transition-all active:scale-95"
          >
            <X size={20} />
          </button>

          {/* Header */}
          <div className="mb-12 text-center">
            <div className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-[2rem] bg-blue-600 text-white shadow-xl shadow-blue-200 dark:shadow-blue-900/40 animate-float">
              <Zap size={40} className="fill-current" />
            </div>
            <h1 className="text-4xl font-black text-slate-900 dark:text-white tracking-tighter">
              Start Your <span className="text-blue-600">Breakthrough</span>
            </h1>
            <p className="mt-3 text-lg font-medium text-slate-500 dark:text-slate-400">
              What incredible concept will you teach us today?
            </p>
          </div>

          {/* Preset Topics */}
          <div className="mb-10">
            <p className="mb-4 text-xs font-black uppercase tracking-[0.2em] text-slate-400 dark:text-slate-500">Popular Subjects</p>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {presetTopics.map((topic, i) => (
                <button
                  key={topic.id}
                  onClick={() => onSelectTopic(topic.label)}
                  className="group relative flex flex-col items-center gap-2 rounded-2xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50 p-4 transition-all hover:bg-white dark:hover:bg-slate-800 hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-xl hover:shadow-blue-100/20 dark:hover:shadow-blue-900/20 hover:-translate-y-1 active:scale-95"
                >
                  <span className={`text-2xl transition-transform group-hover:scale-125 duration-300`}>{topic.icon}</span>
                  <span className="text-sm font-black text-slate-700 dark:text-slate-300">{topic.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="mb-10 flex items-center gap-4">
            <div className="flex-1 border-t border-slate-100 dark:border-slate-800"></div>
            <span className="text-[10px] font-black uppercase tracking-widest text-slate-300 dark:text-slate-700">or enter your own</span>
            <div className="flex-1 border-t border-slate-100 dark:border-slate-800"></div>
          </div>

          {/* Custom Topic Input */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="relative group">
              <div className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-600 group-focus-within:text-blue-600 transition-colors">
                <Search size={20} />
              </div>
              <input
                type="text"
                value={customTopic}
                onChange={(e) => setCustomTopic(e.target.value)}
                placeholder="e.g., Quantum Mechanics, French Revolution..."
                className="w-full rounded-2xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50 py-4 pl-14 pr-6 text-sm font-black text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-600 outline-none transition-all focus:bg-white dark:focus:bg-slate-800 focus:border-blue-600 dark:focus:border-blue-600 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/20 shadow-sm"
              />
            </div>

            <button
              type="submit"
              disabled={!customTopic.trim()}
              className="w-full rounded-2xl bg-slate-900 dark:bg-blue-600 py-5 text-sm font-black text-white shadow-xl shadow-slate-200 dark:shadow-blue-900/20 transition-all hover:bg-blue-600 dark:hover:bg-blue-500 hover:shadow-blue-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 active:scale-95"
            >
              <Sparkles size={18} />
              GENERATE LESSON
            </button>
          </form>

          {/* Footer Info */}
          <div className="mt-10 flex items-center justify-center gap-2">
            <BookOpen size={14} className="text-slate-300 dark:text-slate-700" />
            <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 dark:text-slate-600">
              Adaptive AI Student Engine Active
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopicSelector;
