"use client";

import { X, LogOut, AlertTriangle, Zap, ArrowRight } from "lucide-react";

const EndSessionModal = ({ isOpen, onClose, onConfirm, topic }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="absolute inset-0 bg-slate-900/60 dark:bg-black/80 backdrop-blur-md animate-in fade-in duration-300"
      />

      {/* Modal Container */}
      <div className="relative w-full max-w-lg overflow-hidden rounded-[2.5rem] bg-white dark:bg-slate-900 shadow-2xl animate-fade-in-up border border-slate-200 dark:border-slate-800">
        {/* Decorative Top Bar */}
        <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-blue-600 to-indigo-600"></div>
        
        <div className="relative p-10">
          {/* Close Button */}
          <button
            onClick={onClose}
            className="absolute right-8 top-8 h-10 w-10 flex items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 hover:bg-rose-50 dark:hover:bg-rose-900/40 hover:text-rose-600 transition-all active:scale-95"
          >
            <X size={20} />
          </button>

          {/* Icon */}
          <div className="mb-8 flex h-16 w-16 items-center justify-center rounded-2xl bg-rose-50 dark:bg-rose-900/20 text-rose-600">
            <LogOut size={32} />
          </div>

          {/* Header */}
          <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tighter mb-4 leading-tight">
            Ready to wrap up <br />
            your <span className="text-rose-600">session?</span>
          </h2>
          
          <p className="text-slate-500 dark:text-slate-400 font-medium leading-relaxed mb-10">
            You've done a great job explaining <span className="text-slate-900 dark:text-white font-bold">"{topic}"</span>. Ending the session will generate your final mastery report.
          </p>

          {/* Info Card */}
          <div className="bg-blue-50/50 dark:bg-blue-900/10 rounded-2xl p-5 border border-blue-100/50 dark:border-blue-900/20 mb-10 flex gap-4">
            <div className="h-10 w-10 shrink-0 bg-white dark:bg-slate-800 rounded-xl flex items-center justify-center text-blue-600 shadow-sm">
              <Zap size={20} className="fill-current" />
            </div>
            <div>
              <p className="text-xs font-black text-blue-900 dark:text-blue-400 uppercase tracking-widest mb-1">Deep Evaluation</p>
              <p className="text-[10px] font-bold text-blue-600 dark:text-blue-500 uppercase tracking-widest opacity-70">AI will analyze gaps in your explanation</p>
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-col gap-3">
            <button
              onClick={onConfirm}
              className="w-full rounded-2xl bg-slate-900 dark:bg-blue-600 py-5 text-sm font-black text-white shadow-xl shadow-slate-200 dark:shadow-blue-900/20 transition-all hover:bg-rose-600 dark:hover:bg-rose-600 hover:shadow-rose-200 flex items-center justify-center gap-2 active:scale-95 group"
            >
              YES, GENERATE REPORT
              <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <button
              onClick={onClose}
              className="w-full rounded-2xl bg-slate-100 dark:bg-slate-800 py-5 text-sm font-black text-slate-500 dark:text-slate-400 transition-all hover:bg-slate-200 dark:hover:bg-slate-700 active:scale-95"
            >
              NOT YET, KEEP TEACHING
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EndSessionModal;
