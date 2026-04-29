import { TrendingUp, AlertCircle, CheckCircle2, Zap } from "lucide-react";

const ReportPanel = ({ report, isSessionActive }) => {
  if (!report && isSessionActive) {
    return (
      <div className="space-y-4">
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center">
          <Zap size={32} className="mx-auto mb-2 text-blue-600" />
          <p className="font-semibold text-slate-900">Session Active</p>
          <p className="text-xs text-slate-600">
            Teaching in progress... Report will appear when session ends.
          </p>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-center">
        <p className="text-sm text-slate-500">No report available.</p>
      </div>
    );
  }

  const confidencePercentage = Math.round((report.confidence_score || 0) * 100);
  const scorePercentage = Math.round((report.score || 0) * 10);

  return (
    <div className="space-y-4">
      {/* Header */}
      <div>
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          Learning Report
        </p>
      </div>

      {/* Score Card */}
      <div className="rounded-2xl bg-gradient-to-br from-blue-50 to-blue-100 p-6 shadow-sm">
        <p className="text-sm font-semibold text-blue-900">Understanding Score</p>
        <div className="mt-3 flex items-baseline gap-2">
          <p className="text-4xl font-bold text-blue-600">{scorePercentage}%</p>
          <p className="text-sm text-blue-700">{report.understanding || "Developing"}</p>
        </div>
        <div className="mt-4 h-2 rounded-full bg-blue-200">
          <div
            className="h-full rounded-full bg-blue-600 transition-all"
            style={{ width: `${scorePercentage}%` }}
          ></div>
        </div>
      </div>

      {/* Confidence Indicator */}
      <div className="rounded-2xl border border-slate-200 bg-white p-4">
        <div className="flex items-center justify-between">
          <p className="text-sm font-semibold text-slate-900">AI Confidence</p>
          <span className="text-xs font-bold text-slate-600">
            {confidencePercentage}%
          </span>
        </div>
        <div className="mt-3 h-1.5 rounded-full bg-slate-200">
          <div
            className="h-full rounded-full bg-gradient-to-r from-amber-400 to-green-500 transition-all"
            style={{ width: `${confidencePercentage}%` }}
          ></div>
        </div>
      </div>

      {/* Gaps & Strengths */}
      <div className="space-y-3">
        {report.gaps && report.gaps.length > 0 && (
          <div className="rounded-2xl border border-red-200 bg-red-50 p-4">
            <div className="mb-2 flex items-center gap-2">
              <AlertCircle size={18} className="text-red-600" />
              <p className="font-semibold text-red-900">Areas to Improve</p>
            </div>
            <ul className="space-y-1 text-sm text-red-800">
              {report.gaps.map((gap, idx) => (
                <li key={idx} className="flex gap-2">
                  <span>•</span>
                  <span>{gap}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {report.strengths && report.strengths.length > 0 && (
          <div className="rounded-2xl border border-green-200 bg-green-50 p-4">
            <div className="mb-2 flex items-center gap-2">
              <CheckCircle2 size={18} className="text-green-600" />
              <p className="font-semibold text-green-900">Strengths</p>
            </div>
            <ul className="space-y-1 text-sm text-green-800">
              {report.strengths.map((strength, idx) => (
                <li key={idx} className="flex gap-2">
                  <span>✓</span>
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Feedback */}
      {report.feedback && report.feedback.length > 0 && (
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <p className="mb-2 font-semibold text-slate-900">Feedback</p>
          <ul className="space-y-2 text-xs text-slate-700">
            {report.feedback.map((item, idx) => (
              <li key={idx} className="flex gap-2">
                <span className="mt-1 inline-flex h-1.5 w-1.5 flex-shrink-0 rounded-full bg-slate-400"></span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Progress */}
      {report.progress_state && (
        <div className="rounded-2xl border border-slate-200 bg-white p-4">
          <div className="mb-3 flex items-center gap-2">
            <TrendingUp size={18} className="text-slate-600" />
            <p className="font-semibold text-slate-900">Progress</p>
          </div>
          <div className="space-y-1 text-xs text-slate-600">
            <p>Messages: {report.progress_state.messages_count || 0}</p>
            <p>Turns: {report.progress_state.turns_count || 0}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportPanel;

