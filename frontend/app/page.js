"use client";

import { useState, useEffect, useRef } from "react";
import ChatWindow from "../components/ChatWindow";
import InputBox from "../components/InputBox";
import TopicSelector from "../components/TopicSelector";
import ReportPanel from "../components/ReportPanel";
import ModeToggle from "../components/ModeToggle";
import RescueHint from "../components/RescueHint";
import EndSessionModal from "../components/EndSessionModal";
import CurioAPI from "../utils/api";
import { RotateCcw, LogOut, LayoutDashboard, GraduationCap, CheckCircle2, Zap, Sparkles, BookOpen } from "lucide-react";
import Dashboard from "../components/dashboard/Dashboard";
import LandingPage from "../components/LandingPage";
import ThemeToggle from "../components/ThemeToggle";

export default function Home() {
  // Navigation & Preferences State
  const [currentView, setCurrentView] = useState("landing"); // 'landing', 'learning', 'dashboard'
  const [initialDashboardTab, setInitialDashboardTab] = useState("overview");
  const [settings, setSettings] = useState({
    personality: "Empathetic student",
    difficultyFloor: "Standard",
    voiceEnabled: true,
    darkMode: false,
    notifications: true
  });
  const [mounted, setMounted] = useState(false);

  // Load preferences from localStorage on mount
  useEffect(() => {
    setMounted(true);
    const saved = localStorage.getItem('curio_settings');
    if (saved) {
      setSettings(JSON.parse(saved));
    }
  }, []);

  // Apply Dark Mode & Persist Settings
  useEffect(() => {
    if (settings.darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('curio_settings', JSON.stringify(settings));
  }, [settings]);

  const [showTopicSelector, setShowTopicSelector] = useState(false);
  const [showEndModal, setShowEndModal] = useState(false);
  
  // Learning Session State
  const [sessionActive, setSessionActive] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [topic, setTopic] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentMode, setCurrentMode] = useState("student");
  const [showRescue, setShowRescue] = useState(false);

  // Report State
  const [report, setReport] = useState(null);
  const [sessionEnded, setSessionEnded] = useState(false);
  const [userEmail] = useState("student@curio.ai");

  // Handle topic selection
  const handleSelectTopic = async (selectedTopic) => {
    try {
      setIsLoading(true);
      setTopic(selectedTopic);
      setShowTopicSelector(false);
      const session = await CurioAPI.createSession(selectedTopic, userEmail);
      setSessionId(session.session_id);
      setSessionActive(true);
      setSessionEnded(false);
      setReport(null);
      setMessages([
        {
          role: "ai",
          content: `Session initiated for **${selectedTopic}**. \n\nPlease provide a comprehensive explanation of this concept to begin the instructional evaluation. Your response will establish the baseline for our knowledge synchronization.`,
          ai_intent: "student",
          followups: [
            "Outline the core principles",
            "Define primary objectives",
            "Provide contextual examples",
          ],
        },
      ]);
    } catch (error) {
      console.error("Error starting session:", error);
      alert("Failed to start session. Please try again.");
      setShowTopicSelector(true);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle message sending
  const handleSend = async (content) => {
    if (!content.trim() || isLoading) return;
    const userMessage = { role: "user", content };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    try {
      const response = await CurioAPI.sendMessage(sessionId, content, currentMode);
      if (response.ai_message) {
        setMessages((prev) => [...prev, {
          role: "ai",
          content: response.ai_message,
          ai_intent: response.ai_intent,
          followups: response.followups || []
        }]);
      }
    } catch (error) {
      console.error("Error sending message:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRescue = () => setShowRescue(true);
  const handleApplyHint = (hintContent) => {
    setMessages((prev) => [...prev, {
      role: "ai",
      content: hintContent,
      ai_intent: "hint",
      followups: ["Does this help clarify?", "Shall we continue our explanation?"]
    }]);
  };

  const handleConfirmEndSession = async () => {
    setShowEndModal(false);
    setIsLoading(true);
    try {
      const response = await CurioAPI.evaluateSession(sessionId);
      setReport(response.report);
      setSessionEnded(true);
      setSessionActive(false);
    } catch (error) {
      console.error("Error evaluating session:", error);
      alert("Failed to generate report. Ending session anyway.");
      setSessionEnded(true);
      setSessionActive(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectReport = (selectedReport) => {
    setTopic(selectedReport.topic);
    setReport(selectedReport);
    setSessionEnded(true);
    setSessionActive(false);
    setMessages([]);
    setCurrentView("learning");
  };

  const handleRestart = () => {
    setSessionActive(false);
    setSessionId(null);
    setTopic(null);
    setMessages([]);
    setReport(null);
    setSessionEnded(false);
    setShowTopicSelector(true);
    setCurrentMode("student");
  };

  const handleNewSession = () => {
    handleRestart();
    setCurrentView("learning");
  };

  // If landing page, show only that
  if (currentView === "landing") {
    return (
      <LandingPage 
        onGetStarted={() => setCurrentView("dashboard")} 
        darkMode={settings.darkMode}
        onToggleDarkMode={() => setSettings(s => ({ ...s, darkMode: !s.darkMode }))}
      />
    );
  }

  return (
    <div className="min-h-screen font-outfit selection:bg-blue-500/30 transition-colors duration-700 bg-[#f8fafc] dark:bg-[#020617]">
      {/* Floating Effects */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-1/4 left-10 h-32 w-32 bg-blue-600/5 dark:bg-blue-600/10 blur-[100px] animate-pulse"></div>
        <div className="absolute bottom-1/4 right-10 h-40 w-40 bg-indigo-600/5 dark:bg-indigo-600/10 blur-[120px] animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="view-container relative z-10">
        {currentView === "dashboard" ? (
          <div className="animate-fade-in-up">
            <Dashboard 
              userEmail={userEmail} 
              onSelectReport={handleSelectReport}
              onBackToLearning={handleNewSession}
              globalSettings={settings}
              onUpdateSettings={setSettings}
              initialTab={initialDashboardTab}
            />
          </div>
        ) : (
          <div className="relative animate-fade-in-up">
            {/* Top Navigation Bar */}
            <nav className="sticky top-0 z-40 px-8 py-4 bg-slate-900/5 backdrop-blur-xl border-b border-slate-900/10 dark:bg-[#020617]/80 dark:border-white/10 transition-all duration-700">
              <div className="mx-auto max-w-[1400px] flex items-center justify-between">
                <div className="flex items-center gap-8">
                  <div 
                    onClick={() => setCurrentView("landing")}
                    className="flex items-center gap-2 cursor-pointer group"
                  >
                    <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tighter transition-all group-hover:scale-105">
                      Curio <span className="text-blue-600">AI</span>
                    </h1>
                  </div>
                  
                  <div className="flex items-center gap-1 bg-slate-100/50 dark:bg-slate-900/50 backdrop-blur-md p-1 rounded-2xl border border-slate-200/50 dark:border-slate-800/50">
                    <button 
                      onClick={() => setCurrentView("learning")}
                      className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-black transition-all duration-300 ${currentView === 'learning' ? 'bg-white dark:bg-slate-800 shadow-md text-blue-600 scale-105' : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-white/50'}`}
                    >
                      <GraduationCap size={14} />
                      LEARNING
                    </button>
                    <button 
                      onClick={() => {
                        setInitialDashboardTab("overview");
                        setCurrentView("dashboard");
                      }}
                      className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-black transition-all duration-300 ${currentView === 'dashboard' ? 'bg-white dark:bg-slate-800 shadow-md text-blue-600 scale-105' : 'text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-white/50'}`}
                    >
                      <LayoutDashboard size={14} />
                      DASHBOARD
                    </button>
                  </div>
                </div>

                <div className="flex items-center gap-6">
                  <ThemeToggle 
                    darkMode={settings.darkMode} 
                    onToggle={() => setSettings(s => ({ ...s, darkMode: !s.darkMode }))} 
                  />
                  <button 
                    onClick={handleNewSession}
                    className="hidden sm:flex items-center gap-2 px-8 py-3 rounded-2xl text-xs font-black transition-all active:scale-95 border dark:bg-white/5 dark:backdrop-blur-md dark:border-white/10 dark:text-white dark:hover:bg-white dark:hover:text-slate-900 bg-slate-900/5 backdrop-blur-md border-slate-900/10 text-slate-900 hover:bg-slate-900 hover:text-white"
                  >
                    NEW SESSION
                  </button>
                  <div className="flex items-center gap-3">
                    <div className="text-right hidden sm:block">
                      <p className="text-xs font-black text-slate-900 dark:text-white">Student AI</p>
                      <p className="text-[10px] font-bold text-blue-500 uppercase tracking-widest">Level 12 Scholar</p>
                    </div>
                    <div 
                      onClick={() => {
                        setInitialDashboardTab("profile");
                        setCurrentView("dashboard");
                      }}
                      className="h-10 w-10 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-600 border-2 border-white dark:border-slate-800 shadow-lg overflow-hidden flex items-center justify-center text-white cursor-pointer hover:scale-110 transition-transform active:scale-95"
                    >
                      <GraduationCap size={20} />
                    </div>
                  </div>
                </div>
              </div>
            </nav>

            {/* Loading Overlay */}
            {isLoading && (
              <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 dark:bg-slate-950/80 backdrop-blur-md transition-all duration-300">
                <div className="flex flex-col items-center gap-6">
                  <div className="relative">
                    <div className="h-16 w-16 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
                    <div className="absolute inset-0 h-16 w-16 animate-ping rounded-full border-4 border-blue-400 opacity-20"></div>
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-black text-slate-900 dark:text-white tracking-[0.2em] uppercase">Calibrating Interface</p>
                    <p className="text-[10px] font-bold text-slate-400 mt-1 uppercase">Synchronizing cognitive vectors...</p>
                  </div>
                </div>
              </div>
            )}

            <TopicSelector isOpen={showTopicSelector} onSelectTopic={handleSelectTopic} />
            <RescueHint
              isOpen={showRescue}
              onClose={() => setShowRescue(false)}
              onApplyHint={handleApplyHint}
              currentTopic={topic}
            />
            <EndSessionModal
              isOpen={showEndModal}
              onClose={() => setShowEndModal(false)}
              onConfirm={handleConfirmEndSession}
              topic={topic}
            />

            {/* Main Content */}
            <div className="mx-auto max-w-[1400px] px-8">
              {sessionActive || messages.length > 0 ? (
                <div className="py-10">
                  <div className="mb-10 flex flex-col items-start justify-between gap-6 lg:flex-row lg:items-center">
                    <div>
                      <div className="flex items-center gap-3 mb-3">
                        <span className="bg-blue-600/10 text-blue-600 text-[10px] font-black px-3 py-1 rounded-full border border-blue-200/50 dark:border-blue-800 uppercase tracking-[0.2em]">ACTIVE EVALUATION</span>
                        <span className="text-slate-300 dark:text-slate-700">/</span>
                        <span className="text-slate-500 dark:text-slate-400 text-[10px] font-black uppercase tracking-[0.2em]">{topic}</span>
                      </div>
                      <h2 className="text-5xl font-black text-slate-900 dark:text-white tracking-tighter leading-tight uppercase">
                        INSTRUCTION: <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">{topic}</span>
                      </h2>
                    </div>

                    <div className="flex flex-wrap items-center gap-4">
                      {sessionActive && !sessionEnded && (
                        <ModeToggle
                          currentMode={currentMode}
                          onModeChange={setCurrentMode}
                        />
                      )}
                      {sessionActive && !sessionEnded && (
                        <button
                          onClick={() => setShowEndModal(true)}
                          disabled={isLoading}
                          className="group flex items-center gap-2 rounded-[2.5rem] bg-slate-900/5 dark:bg-white/5 border border-slate-900/10 dark:border-white/10 px-8 py-4 text-sm font-black text-slate-700 dark:text-white transition-all hover:bg-rose-500 hover:text-white hover:border-rose-500 dark:hover:bg-rose-500 dark:hover:border-rose-500 disabled:opacity-50 shadow-sm active:scale-95 backdrop-blur-md"
                        >
                          <LogOut size={18} className="group-hover:translate-x-1 transition-transform" />
                          END SESSION
                        </button>
                      )}
                      {sessionEnded && (
                        <button
                          onClick={handleRestart}
                          className="flex items-center gap-3 rounded-[2rem] bg-slate-900 dark:bg-blue-600 px-10 py-5 text-sm font-black text-white transition-all hover:bg-blue-600 dark:hover:bg-blue-500 hover:shadow-2xl hover:shadow-blue-200 shadow-xl shadow-slate-200 active:scale-95"
                        >
                          <RotateCcw size={18} />
                          START NEW TOPIC
                        </button>
                      )}
                    </div>
                  </div>

                  <div className="grid gap-10 lg:grid-cols-12 items-start">
                    <div className="lg:col-span-7 xl:col-span-8 space-y-6">
                      <div className="rounded-[3rem] bg-white dark:bg-slate-900/60 p-2 shadow-[0_20px_50px_rgba(0,0,0,0.02)] border border-slate-100 dark:border-white/5 backdrop-blur-md">
                        <div className="rounded-[2.5rem] bg-slate-50/50 dark:bg-slate-900/40 p-6">
                          <ChatWindow messages={messages} />
                        </div>
                      </div>
                      {sessionActive && !sessionEnded && (
                        <InputBox onSend={handleSend} onRescue={handleRescue} />
                      )}
                      {sessionEnded && (
                        <div className="rounded-[3rem] bg-gradient-to-br from-emerald-500 to-teal-600 p-10 text-center text-white shadow-2xl shadow-emerald-200/50 relative overflow-hidden animate-fade-in-up">
                          <div className="absolute top-0 right-0 p-10 opacity-10">
                            <CheckCircle2 size={120} />
                          </div>
                          <div className="relative z-10">
                            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-white/20 backdrop-blur-md mb-6">
                              <CheckCircle2 size={40} />
                            </div>
                            <h3 className="text-3xl font-black tracking-tight mb-2">Evaluation Finalized</h3>
                            <p className="text-emerald-50 text-lg opacity-90 font-medium max-w-lg mx-auto">
                              The instructional session for {topic} has been processed. Review the comprehensive report to assess instructional efficacy.
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                    <div className="lg:col-span-5 xl:col-span-4 sticky top-28">
                      <ReportPanel
                        report={report}
                        isSessionActive={sessionActive && !sessionEnded}
                      />
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
                  <div className="relative animate-float">
                    <div className="h-32 w-32 bg-blue-600 text-white rounded-[2.5rem] flex items-center justify-center mb-10 shadow-2xl shadow-blue-200 transform -rotate-6">
                      <GraduationCap size={64} />
                    </div>
                    <div className="absolute -top-4 -right-4 h-12 w-12 bg-amber-400 rounded-2xl flex items-center justify-center text-white shadow-lg animate-bounce">
                      <Sparkles size={24} />
                    </div>
                  </div>
                  
                  <div className="animate-fade-in-up">
                    <h2 className="text-6xl font-black text-slate-900 dark:text-white tracking-tighter mb-6 leading-tight uppercase">
                      INITIALIZE <br />
                      INSTRUCTIONAL <span className="text-blue-600">PIPELINE</span>
                    </h2>
                    <p className="text-slate-500 dark:text-slate-400 text-sm font-bold uppercase tracking-[0.1em] max-w-md leading-relaxed mb-12 mx-auto">
                      Select a subject matter to commence the role-reversal evaluation process.
                    </p>
                    <button 
                      onClick={handleNewSession}
                      className="group relative flex items-center justify-center gap-4 px-12 py-7 rounded-[2.5rem] font-black text-xl transition-all shadow-2xl active:scale-95 tracking-tighter dark:bg-blue-600 dark:text-white dark:shadow-blue-600/30 dark:hover:bg-blue-500 dark:hover:scale-105 bg-slate-900 text-white shadow-slate-900/20 hover:bg-slate-800 hover:scale-105 mx-auto"
                    >
                      <Zap size={22} className="fill-current" />
                      SELECT SUBJECT
                    </button>
                  </div>

                  <div className="absolute top-1/4 left-10 opacity-10 animate-float hidden xl:block">
                    <BookOpen size={100} className="text-blue-600" />
                  </div>
                  <div className="absolute bottom-1/4 right-10 opacity-10 animate-float hidden xl:block" style={{ animationDelay: '1s' }}>
                    <Zap size={80} className="text-indigo-600" />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
