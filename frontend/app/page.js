"use client";

import { useState, useEffect } from "react";
import ChatWindow from "../components/ChatWindow";
import InputBox from "../components/InputBox";
import ReportPanel from "../components/ReportPanel";
import TopicSelector from "../components/TopicSelector";
import ModeToggle from "../components/ModeToggle";
import RescueHint from "../components/RescueHint";
import CurioAPI from "../utils/api";
import { RotateCcw, LogOut } from "lucide-react";

export default function Home() {
  // Session State
  const [sessionActive, setSessionActive] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [topic, setTopic] = useState(null);

  // Chat State
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Mode State
  const [currentMode, setCurrentMode] = useState("student");

  // UI State
  const [showTopicSelector, setShowTopicSelector] = useState(true);
  const [showRescue, setShowRescue] = useState(false);

  // Report State
  const [report, setReport] = useState(null);
  const [sessionEnded, setSessionEnded] = useState(false);

  // Handle topic selection
  const handleSelectTopic = async (selectedTopic) => {
    try {
      setIsLoading(true);
      setTopic(selectedTopic);
      setShowTopicSelector(false);

      // Create session on backend
      const session = await CurioAPI.createSession(selectedTopic);
      setSessionId(session.session_id);
      setSessionActive(true);

      // Add initial AI message
      setMessages([
        {
          role: "ai",
          content: `Great! Let's explore "${selectedTopic}" together. I'm excited to learn from you! 🎓\n\nCould you please explain this topic in your own words? Tell me what you understand about it. This helps me see what you already know!`,
          ai_intent: "question",
          followups: [
            "What are the main concepts?",
            "How would you define it?",
            "What examples do you think of?",
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

  // Handle sending message
  const handleSend = async (message) => {
    if (!sessionId || isLoading) return;

    try {
      setIsLoading(true);

      // Add user message
      const userMessage = { role: "user", content: message };
      setMessages((prev) => [...prev, userMessage]);

      // Send to backend
      const response = await CurioAPI.sendMessage(
        sessionId,
        message,
        currentMode,
        { topic }
      );

      // Add AI response
      const aiMessage = {
        role: "ai",
        content: response.ai_message,
        ai_intent: response.ai_intent || "question",
        followups: response.followups || [],
      };
      setMessages((prev) => [...prev, aiMessage]);

      // Check if termination offer
      if (response.termination_offer) {
        setReport(response);
        setSessionEnded(true);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = {
        role: "ai",
        content: "Sorry, I encountered an error. Please try again.",
        ai_intent: "error",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle rescue/hint
  const handleRescue = () => {
    setShowRescue(true);
  };

  const handleApplyHint = (action) => {
    const hintMessages = {
      break_down:
        "Let's start simpler. What are the most basic building blocks of this concept?",
      example: "Can you think of a real-world situation where this concept applies?",
      reset: "No problem! Let's start fresh. Go ahead and explain the topic as if you're starting from the beginning.",
    };

    const hintMessage = {
      role: "ai",
      content: hintMessages[action],
      ai_intent: "hint",
    };
    setMessages((prev) => [...prev, hintMessage]);
  };

  // Handle mode change
  const handleModeChange = (newMode) => {
    setCurrentMode(newMode);

    const modeMessages = {
      student: "Now in Student Mode! I'll ask challenging questions. 🤔",
      rescue: "Switched to Rescue Mode! I'll be gentler and provide guidance. 💡",
      evaluator: "Evaluator Mode activated! Preparing your learning report... 📊",
    };

    const modeMessage = {
      role: "ai",
      content: modeMessages[newMode],
      ai_intent: "acknowledgment",
    };
    setMessages((prev) => [...prev, modeMessage]);
  };

  // Handle end session
  const handleEndSession = async () => {
    if (!sessionId) return;

    try {
      setIsLoading(true);
      const evaluation = await CurioAPI.evaluateSession(sessionId);
      setReport(evaluation);
      setSessionEnded(true);
      setSessionActive(false);

      const endMessage = {
        role: "ai",
        content: `Thank you for teaching me! Your understanding score is ${Math.round((evaluation.confidence_score || 0) * 100)}%. ${evaluation.feedback?.[0] || "Great effort!"}`,
        ai_intent: "acknowledgment",
      };
      setMessages((prev) => [...prev, endMessage]);
    } catch (error) {
      console.error("Error ending session:", error);
      alert("Error ending session. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Handle restart
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 text-slate-900">
      {/* Topic Selector Modal */}
      <TopicSelector isOpen={showTopicSelector} onSelectTopic={handleSelectTopic} />

      {/* Rescue Hint Modal */}
      <RescueHint
        isOpen={showRescue}
        onClose={() => setShowRescue(false)}
        onApplyHint={handleApplyHint}
        currentTopic={topic}
      />

      {/* Main Content */}
      {sessionActive || messages.length > 0 ? (
        <div className="mx-auto max-w-[1400px] px-4 py-8 sm:px-6 lg:px-8">
          {/* Header with Controls */}
          <div className="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">
                <span className="text-blue-600">Curio</span> Learning Session
              </h1>
              {topic && (
                <p className="mt-1 text-slate-600">
                  Topic: <span className="font-semibold">{topic}</span>
                </p>
              )}
            </div>

            {/* Controls */}
            <div className="flex flex-col items-end gap-3">
              {sessionActive && !sessionEnded && (
                <ModeToggle
                  currentMode={currentMode}
                  onModeChange={handleModeChange}
                />
              )}

              {sessionActive && !sessionEnded && (
                <button
                  onClick={handleEndSession}
                  disabled={isLoading}
                  className="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:bg-slate-50 disabled:opacity-50"
                >
                  <LogOut size={16} />
                  End Session
                </button>
              )}

              {sessionEnded && (
                <button
                  onClick={handleRestart}
                  className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700"
                >
                  <RotateCcw size={16} />
                  New Session
                </button>
              )}
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid gap-8 lg:grid-cols-3">
            {/* Chat Section */}
            <div className="lg:col-span-2 space-y-4">
              <div className="rounded-3xl bg-white p-6 shadow-[0_30px_60px_-30px_rgba(15,23,42,0.15)]">
                <ChatWindow messages={messages} />
              </div>

              {sessionActive && !sessionEnded && (
                <InputBox onSend={handleSend} onRescue={handleRescue} />
              )}

              {sessionEnded && (
                <div className="rounded-2xl border border-green-200 bg-green-50 p-6 text-center">
                  <p className="text-lg font-semibold text-green-900">
                    ✅ Session Complete!
                  </p>
                  <p className="mt-1 text-sm text-green-700">
                    Your learning report is ready below.
                  </p>
                </div>
              )}
            </div>

            {/* Report Section */}
            <div className="rounded-3xl bg-white p-6 shadow-[0_30px_60px_-30px_rgba(15,23,42,0.15)]">
              <ReportPanel
                report={report}
                isSessionActive={sessionActive && !sessionEnded}
              />
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

