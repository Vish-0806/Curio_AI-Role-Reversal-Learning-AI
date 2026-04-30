"use client";

import { Moon, Sun } from "lucide-react";

const ThemeToggle = ({ darkMode, onToggle }) => {
  return (
    <button
      onClick={onToggle}
      className={`
        relative flex items-center gap-3 px-4 py-2 rounded-2xl transition-all duration-500
        ${darkMode 
          ? "bg-slate-900 border border-slate-800 text-slate-400 hover:text-white" 
          : "bg-white border border-slate-200 text-slate-500 hover:text-slate-900 shadow-sm"}
      `}
    >
      <div className="relative h-5 w-5 flex items-center justify-center">
        {darkMode ? (
          <Moon size={18} className="animate-in fade-in zoom-in duration-500" />
        ) : (
          <Sun size={18} className="animate-in fade-in zoom-in duration-500" />
        )}
      </div>
      <span className="text-[10px] font-black uppercase tracking-widest hidden sm:block">
        {darkMode ? "Dark Mode" : "Light Mode"}
      </span>
      
      {/* Switch Track */}
      <div className={`
        w-8 h-4 rounded-full relative transition-colors duration-300 ml-1
        ${darkMode ? 'bg-blue-600' : 'bg-slate-200'}
      `}>
        <div className={`
          absolute top-0.5 w-3 h-3 bg-white rounded-full transition-all duration-300
          ${darkMode ? 'left-4.5' : 'left-0.5'}
        `} style={{ left: darkMode ? '1.125rem' : '0.125rem' }}></div>
      </div>
    </button>
  );
};

export default ThemeToggle;
