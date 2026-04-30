"use client";

import { useEffect, useState } from "react";
import UnicornScene from "unicornstudio-react";
import { Zap, Sparkles, ArrowRight, BrainCircuit, GraduationCap } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

export default function LandingPage({ onGetStarted, darkMode, onToggleDarkMode }) {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  return (
    <div className={`relative min-h-screen w-full overflow-hidden transition-colors duration-700 font-outfit selection:bg-blue-500/30 ${darkMode ? 'bg-[#020617]' : 'bg-[#f8fafc]'}`}>
      {/* Background Section using the exact code provided */}
      <div className={`absolute inset-0 z-0 opacity-100 pointer-events-none flex items-center justify-center transition-all duration-700 ${darkMode ? 'mix-blend-screen' : 'mix-blend-multiply opacity-40'}`}>
        <UnicornScene
          projectId="dtHxoQb8DWIsDjdEWk0d"
          width="1440px"
          height="900px"
          scale={1}
          dpi={1.5}
          sdkUrl="https://cdn.jsdelivr.net/gh/hiunicornstudio/unicornstudio.js@2.1.11/dist/unicornStudio.umd.js"
        />
      </div>

      {/* Floating Effects */}
      <div className="absolute inset-0 z-1 pointer-events-none">
        <div className={`absolute top-1/4 left-10 h-32 w-32 ${darkMode ? 'bg-blue-600/10' : 'bg-blue-600/5'} blur-[100px] animate-pulse`}></div>
        <div className={`absolute bottom-1/4 right-10 h-40 w-40 ${darkMode ? 'bg-indigo-600/10' : 'bg-indigo-600/5'} blur-[120px] animate-pulse`} style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 px-12 py-8 flex items-center justify-between transition-all duration-1000 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-10'}`}>
        <div className="flex items-center gap-3 group cursor-pointer">
          <div className="h-12 w-12 bg-blue-600 rounded-2xl flex items-center justify-center text-white shadow-2xl shadow-blue-500/20 transition-transform hover:rotate-12">
            <GraduationCap size={28} />
          </div>
          <h1 className={`text-4xl font-black tracking-tighter transition-colors ${darkMode ? 'text-white' : 'text-slate-900'}`}>
            CURIO <span className="text-blue-600">AI</span>
          </h1>
        </div>

        <div className="hidden md:flex items-center gap-6">
          <ThemeToggle darkMode={darkMode} onToggle={onToggleDarkMode} />
          <button 
            onClick={onGetStarted}
            className={`px-8 py-3 rounded-2xl text-xs font-black transition-all active:scale-95 border ${darkMode ? 'bg-white/5 backdrop-blur-md border-white/10 text-white hover:bg-white hover:text-slate-900' : 'bg-slate-900/5 backdrop-blur-md border-slate-900/10 text-slate-900 hover:bg-slate-900 hover:text-white'}`}
          >
            AUTHENTICATE
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 flex flex-col items-center justify-end min-h-screen text-center px-6 pb-10">
        <div className={`transition-all duration-1000 delay-300 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-20'}`}>
          {/* CTA Button */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
            <button 
              onClick={onGetStarted}
              className={`group relative flex items-center gap-4 px-12 py-7 rounded-[2.5rem] font-black text-xl transition-all shadow-2xl active:scale-95 tracking-tighter ${darkMode ? 'bg-blue-600 text-white shadow-blue-600/30 hover:bg-blue-500 hover:scale-105' : 'bg-slate-900 text-white shadow-slate-900/20 hover:bg-slate-800 hover:scale-105'}`}
            >
              <Zap size={22} className="fill-current" />
              BEGIN EVALUATION
              <ArrowRight size={22} className="group-hover:translate-x-2 transition-transform" />
            </button>
          </div>
        </div>
      </main>

      {/* Decorative Grid */}
      <div className={`absolute inset-0 z-1 pointer-events-none opacity-20 transition-opacity ${darkMode ? 'opacity-20' : 'opacity-10'}`} 
           style={{ backgroundImage: `radial-gradient(circle at 2px 2px, ${darkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.1)'} 1px, transparent 0)`, backgroundSize: '40px 40px' }}>
      </div>

      {/* Bottom Glow */}
      <div className={`absolute -bottom-1/2 left-1/2 -translate-x-1/2 w-full h-full rounded-full pointer-events-none blur-[200px] transition-colors duration-700 ${darkMode ? 'bg-blue-600/20' : 'bg-blue-600/10'}`}></div>
    </div>
  );
}
