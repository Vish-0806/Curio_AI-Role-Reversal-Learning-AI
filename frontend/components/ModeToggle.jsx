"use client";

import { BookOpen, HelpCircle, Zap } from "lucide-react";
import { useState } from "react";

const ModeToggle = ({ currentMode, onModeChange }) => {
  const [showTooltip, setShowTooltip] = useState(null);

  const modes = [
    {
      id: "student",
      label: "Student Mode",
      icon: BookOpen,
      color: "blue",
      description: "AI asks questions to test your understanding",
    },
    {
      id: "rescue",
      label: "Rescue Mode",
      icon: HelpCircle,
      color: "amber",
      description: "Get hints and gentle guidance",
    },
    {
      id: "evaluator",
      label: "Evaluator Mode",
      icon: Zap,
      color: "purple",
      description: "Get comprehensive assessment",
    },
  ];

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
        Mode:
      </span>
      <div className="flex gap-2">
        {modes.map((mode) => {
          const Icon = mode.icon;
          const isActive = currentMode === mode.id;
          const colorClass =
            mode.color === "blue"
              ? "text-blue-600"
              : mode.color === "amber"
                ? "text-amber-600"
                : "text-purple-600";

          return (
            <div key={mode.id} className="relative">
              <button
                onClick={() => onModeChange(mode.id)}
                onMouseEnter={() => setShowTooltip(mode.id)}
                onMouseLeave={() => setShowTooltip(null)}
                className={`rounded-full p-2 transition ${
                  isActive
                    ? "bg-slate-100 shadow-md"
                    : "bg-white hover:bg-slate-50"
                } border ${isActive ? "border-slate-300" : "border-slate-200"}`}
              >
                <Icon size={18} className={colorClass} />
              </button>

              {/* Tooltip */}
              {showTooltip === mode.id && (
                <div className="absolute bottom-full right-0 mb-2 w-48 rounded-xl bg-slate-900 px-3 py-2 text-sm text-white shadow-lg">
                  <p className="font-semibold">{mode.label}</p>
                  <p className="text-xs text-slate-300">{mode.description}</p>
                  <div className="absolute top-full right-4 h-2 w-2 rotate-45 bg-slate-900"></div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ModeToggle;
