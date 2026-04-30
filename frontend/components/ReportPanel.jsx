"use client";

import { useState } from "react";
import { TrendingUp, AlertCircle, CheckCircle2, Zap, ChevronDown, ChevronUp, Star, Lightbulb } from "lucide-react";

const ReportPanel = ({ report, isSessionActive }) => {
  const [expandedSection, setExpandedSection] = useState(null);

  if (!report && isSessionActive) {
    return (
      <div className="space-y-6">
        <div className="relative overflow-hidden rounded-3xl border border-blue-100 bg-white p-8 text-center shadow-xl">
          <div className="absolute -right-8 -top-8 h-24 w-24 rounded-full bg-blue-50/50 blur-2xl"></div>
          <div className="absolute -bottom-8 -left-8 h-24 w-24 rounded-full bg-indigo-50/50 blur-2xl"></div>
          
          <div className="relative flex flex-col items-center">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-50 text-blue-600 animate-pulse">
              <Zap size={32} />
            </div>
            <h3 className="text-xl font-bold text-slate-900">Session in Progress</h3>
            <p className="mt-2 text-sm leading-relaxed text-slate-500">
              Our AI is currently analyzing your teaching patterns. Your personalized insight report will appear here once the session concludes.
            </p>
            <div className="mt-6 flex gap-2">
              {[0, 1, 2].map((i) => (
                <div key={i} className="h-1.5 w-1.5 rounded-full bg-blue-400 animate-bounce" style={{ animationDelay: `${i * 0.2}s` }}></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="flex flex-col items-center justify-center rounded-3xl border-2 border-dashed border-slate-200 bg-slate-50/50 p-12 text-center">
        <div className="mb-4 text-slate-300">
          <TrendingUp size={48} />
        </div>
        <p className="text-sm font-medium text-slate-500">Ready to analyze your learning progress.</p>
      </div>
    );
  }

  const masteryScore = Math.round(report.understanding_score ?? report.overall_confidence ?? report.confidence_score ?? 0);
  const masteryLevel = report.mastery_level || (masteryScore >= 85 ? "Mastery" : masteryScore >= 70 ? "Proficient" : masteryScore >= 50 ? "Developing" : "Beginner");

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const Section = ({ id, icon: Icon, title, color, count, children, defaultExpanded = false }) => {
    const isExpanded = expandedSection === id || (expandedSection === null && defaultExpanded);
    const colors = {
      emerald: "bg-emerald-50 text-emerald-700 border-emerald-100",
      amber: "bg-amber-50 text-amber-700 border-amber-100",
      rose: "bg-rose-50 text-rose-700 border-rose-100",
      blue: "bg-blue-50 text-blue-700 border-blue-100",
      slate: "bg-slate-50 text-slate-700 border-slate-200",
    };

    return (
      <div className={`overflow-hidden rounded-2xl border transition-all duration-300 ${isExpanded ? "shadow-md" : "shadow-sm hover:shadow-md"} ${colors[color] || colors.slate}`}>
        <button 
          onClick={() => toggleSection(id)}
          className="flex w-full items-center justify-between p-4 font-bold outline-none"
        >
          <div className="flex items-center gap-3">
            <div className={`flex h-8 w-8 items-center justify-center rounded-lg bg-white/80 shadow-sm`}>
              <Icon size={18} />
            </div>
            <div className="flex flex-col items-start">
              <span className="text-sm uppercase tracking-wider">{title}</span>
              {count > 0 && <span className="text-[10px] opacity-70">{count} items identified</span>}
            </div>
          </div>
          {isExpanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
        </button>
        
        <div className={`transition-all duration-300 ease-in-out ${isExpanded ? "max-height-1000 p-4 pt-0" : "max-h-0 opacity-0 overflow-hidden"}`}>
          <div className="h-px w-full bg-current opacity-10 mb-4"></div>
          {children}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Learning Analytics</h2>
        <div className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
      </div>

      {/* Score Card */}
      <div className="group relative overflow-hidden rounded-[2rem] bg-slate-900 p-8 text-white shadow-2xl transition-all duration-500 hover:-translate-y-1">
        <div className="absolute -right-12 -top-12 h-40 w-40 rounded-full bg-blue-600/20 blur-3xl transition-all duration-500 group-hover:scale-150"></div>
        <div className="absolute -left-12 -bottom-12 h-40 w-40 rounded-full bg-indigo-600/20 blur-3xl transition-all duration-500 group-hover:scale-150"></div>
        
        <div className="relative flex items-end justify-between">
          <div>
            <p className="text-[10px] font-black uppercase tracking-widest text-slate-400">Knowledge Depth</p>
            <div className="mt-1 flex items-baseline gap-3">
              <span className="text-6xl font-black tracking-tighter">{masteryScore}%</span>
              <span className={`text-sm font-bold uppercase tracking-widest px-3 py-1 rounded-full bg-white/10 backdrop-blur-md`}>
                {masteryLevel}
              </span>
            </div>
          </div>
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-white/10 backdrop-blur-md">
            <TrendingUp size={32} className="text-blue-400" />
          </div>
        </div>

        <div className="mt-8">
          <div className="flex justify-between text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-2">
            <span>Progress</span>
            <span>{masteryScore}% to Mastery</span>
          </div>
          <div className="h-3 overflow-hidden rounded-full bg-white/5 p-1 ring-1 ring-white/10">
            <div
              className="h-full rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-1000 ease-out shadow-[0_0_15px_rgba(59,130,246,0.5)]"
              style={{ width: `${masteryScore}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      {report.summary && (
        <div className="relative rounded-2xl border border-slate-200 bg-white p-5 shadow-sm overflow-hidden group">
          <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
          <div className="flex gap-4">
            <div className="text-blue-500 mt-1 shrink-0">
              <Star size={20} />
            </div>
            <p className="text-sm italic leading-relaxed text-slate-600 font-medium">
              "{report.summary}"
            </p>
          </div>
        </div>
      )}

      {/* Interactive Insights */}
      <div className="space-y-3">
        <Section 
          id="strengths" 
          icon={CheckCircle2} 
          title="Mastered Concepts" 
          color="emerald" 
          count={report.strengths?.length}
          defaultExpanded
        >
          <ul className="space-y-3">
            {report.strengths?.map((s, idx) => (
              <li key={idx} className="flex gap-3 text-sm text-emerald-900 group">
                <div className="flex-shrink-0 mt-1 h-1.5 w-1.5 rounded-full bg-emerald-500 group-hover:scale-150 transition-transform"></div>
                <span className="leading-relaxed font-medium">{s}</span>
              </li>
            ))}
          </ul>
        </Section>

        <Section 
          id="gaps" 
          icon={AlertCircle} 
          title="Growth Areas" 
          color="amber" 
          count={report.gaps?.length}
        >
          <ul className="space-y-3">
            {report.gaps?.map((g, idx) => (
              <li key={idx} className="flex gap-3 text-sm text-amber-900 group">
                <div className="flex-shrink-0 mt-1 h-1.5 w-1.5 rounded-full bg-amber-500 group-hover:scale-150 transition-transform"></div>
                <span className="leading-relaxed font-medium">{g}</span>
              </li>
            ))}
          </ul>
        </Section>

        {((report.assumptions && report.assumptions.length > 0) || (report.misconceptions && report.misconceptions.length > 0)) && (
          <Section 
            id="misconceptions" 
            icon={Zap} 
            title="Misconceptions" 
            color="rose" 
            count={(report.assumptions?.length || 0) + (report.misconceptions?.length || 0)}
          >
            <ul className="space-y-3">
              {[...(report.assumptions || []), ...(report.misconceptions || [])].map((a, idx) => (
                <li key={idx} className="flex gap-3 text-sm text-rose-900 group">
                  <div className="flex-shrink-0 mt-1 h-1.5 w-1.5 rounded-full bg-rose-500 group-hover:scale-150 transition-transform"></div>
                  <span className="leading-relaxed font-medium">{a}</span>
                </li>
              ))}
            </ul>
          </Section>
        )}

        <Section 
          id="roadmap" 
          icon={Lightbulb} 
          title="Next Steps" 
          color="blue" 
          count={report.recommendations?.length}
        >
          <div className="space-y-3">
            {report.recommendations?.map((r, idx) => (
              <div key={idx} className="flex items-center gap-4 rounded-xl bg-white p-3 shadow-sm transition-all hover:translate-x-1">
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-blue-50 text-xs font-black text-blue-600">
                  {idx + 1}
                </div>
                <p className="text-xs font-bold text-slate-700 leading-tight">{r}</p>
              </div>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
};

export default ReportPanel;
