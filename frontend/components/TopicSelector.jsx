"use client";

import { useState } from "react";
import { X, Zap } from "lucide-react";

const TopicSelector = ({ onSelectTopic, isOpen }) => {
  const [customTopic, setCustomTopic] = useState("");
  const [selectedPreset, setSelectedPreset] = useState(null);

  const presetTopics = [
    { id: "ohms_law", label: "Ohm's Law", icon: "⚡" },
    { id: "photosynthesis", label: "Photosynthesis", icon: "🌱" },
    { id: "water_cycle", label: "Water Cycle", icon: "💧" },
    { id: "gravity", label: "Gravity", icon: "🌍" },
    { id: "evolution", label: "Evolution", icon: "🧬" },
    { id: "calculus", label: "Calculus", icon: "∫" },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    const topic = customTopic.trim() || selectedPreset;
    if (topic) {
      onSelectTopic(topic);
      setCustomTopic("");
      setSelectedPreset(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="relative w-full max-w-2xl rounded-3xl bg-white p-8 shadow-2xl">
        {/* Close Button */}
        <button
          onClick={() => window.location.reload()}
          className="absolute right-6 top-6 text-slate-400 hover:text-slate-600"
        >
          <X size={24} />
        </button>

        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mb-3 flex justify-center">
            <Zap size={48} className="text-blue-600" />
          </div>
          <h1 className="text-4xl font-bold text-slate-900">
            Welcome to <span className="text-blue-600">Curio</span>
          </h1>
          <p className="mt-2 text-lg text-slate-600">
            What would you like to learn about today?
          </p>
        </div>

        {/* Preset Topics */}
        <div className="mb-6">
          <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-slate-500">
            Popular Topics
          </p>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {presetTopics.map((topic) => (
              <button
                key={topic.id}
                onClick={() => setSelectedPreset(topic.id)}
                className={`rounded-2xl px-4 py-3 transition ${
                  selectedPreset === topic.id
                    ? "bg-blue-600 text-white shadow-lg"
                    : "border border-slate-200 bg-slate-50 text-slate-900 hover:border-blue-300 hover:bg-blue-50"
                }`}
              >
                <span className="mr-2">{topic.icon}</span>
                {topic.label}
              </button>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div className="mb-6 flex items-center gap-3">
          <div className="flex-1 border-t border-slate-200"></div>
          <span className="text-sm text-slate-500">or</span>
          <div className="flex-1 border-t border-slate-200"></div>
        </div>

        {/* Custom Topic Input */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-semibold text-slate-600">
              Enter Your Topic
            </label>
            <input
              type="text"
              value={customTopic}
              onChange={(e) => {
                setCustomTopic(e.target.value);
                setSelectedPreset(null);
              }}
              placeholder="e.g., Quantum Mechanics, French Revolution..."
              className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 placeholder-slate-400 outline-none transition focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!customTopic.trim() && !selectedPreset}
            className="w-full rounded-2xl bg-blue-600 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Start Learning
          </button>
        </form>

        {/* Footer Info */}
        <p className="mt-6 text-center text-sm text-slate-500">
          You teach. AI questions. You learn deeply.
        </p>
      </div>
    </div>
  );
};

export default TopicSelector;
