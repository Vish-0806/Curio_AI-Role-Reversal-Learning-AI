"use client";

import { BookOpen, HelpCircle, Zap, Shield } from "lucide-react";
import { useState } from "react";

const ModeToggle = ({ currentMode, onModeChange }) => {
  const modes = [
    {
      id: "student",
      label: "Student",
      icon: BookOpen,
      color: "blue",
    },
    {
      id: "teacher",
      label: "Teacher",
      icon: HelpCircle,
      color: "blue",
    },
    {
      id: "rescue",
      label: "Rescue",
      icon: Shield,
      color: "blue",
    },
    {
      id: "evaluator",
      label: "Evaluator",
      icon: Zap,
      color: "blue",
    },
  ];

  return (
    <div className="rounded-[1.5rem] bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl p-1.5 border border-slate-200/50 dark:border-slate-800 shadow-xl transition-all duration-500">
      <div className="flex gap-1">
        {modes.map((mode) => {
          const Icon = mode.icon;
          const isActive = currentMode === mode.id;

          return (
            <button
              key={mode.id}
              onClick={() => onModeChange(mode.id)}
              className={`
                group relative flex flex-col items-center gap-1.5 rounded-2xl px-5 py-3 transition-all duration-300 min-w-[90px]
                ${isActive 
                  ? "bg-slate-900 dark:bg-blue-600 text-white shadow-2xl shadow-blue-100 dark:shadow-blue-900/20 scale-105" 
                  : "bg-transparent text-slate-500 dark:text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white border border-transparent"}
              `}
            >
              <div className={`
                transition-transform duration-300 group-hover:rotate-6
                ${isActive ? "scale-110" : ""}
              `}>
                <Icon size={18} strokeWidth={isActive ? 2.5 : 2} />
              </div>
              <span className={`text-[9px] font-black uppercase tracking-[0.15em] transition-all duration-300`}>
                {mode.label}
              </span>
              
              {isActive && (
                <div className="absolute -bottom-1 left-1/2 h-1.5 w-1.5 -translate-x-1/2 rounded-full bg-blue-500 dark:bg-white animate-pulse" />
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default ModeToggle;
