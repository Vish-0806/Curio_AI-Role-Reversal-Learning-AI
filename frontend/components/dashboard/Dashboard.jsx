"use client";

import { useState, useEffect } from "react";
import { 
  BarChart3, 
  Clock, 
  FileText, 
  User as UserIcon, 
  Settings, 
  ChevronRight, 
  Search,
  ArrowUpRight,
  BrainCircuit,
  GraduationCap,
  TrendingUp,
  Star,
  LogOut,
  Sparkles,
  Zap,
  Check,
  Shield,
  Moon,
  Volume2
} from "lucide-react";
import CurioAPI from "../../utils/api";

const Dashboard = ({ userEmail, onSelectReport, onBackToLearning, globalSettings, onUpdateSettings, initialTab = "overview" }) => {
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [currentTab, setCurrentTab] = useState(initialTab);

  useEffect(() => {
    setCurrentTab(initialTab);
  }, [initialTab]);
  
  useEffect(() => {
    const fetchReports = async () => {
      try {
        setIsLoading(true);
        const data = await CurioAPI.listUserReports(userEmail);
        setReports(data || []);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchReports();
  }, [userEmail]);

  const filteredReports = reports.filter(r => 
    r.topic.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const stats = {
    totalSessions: reports.length,
    avgScore: reports.length > 0 
      ? Math.round(reports.reduce((acc, r) => acc + (r.understanding_score || 0), 0) / reports.length) 
      : 0,
    topTopic: reports.length > 0 
      ? reports.reduce((prev, current) => (prev.understanding_score > current.understanding_score) ? prev : current).topic 
      : "None yet"
  };

  const handleToggleSetting = (key) => {
    onUpdateSettings(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleSelectSetting = (key, value) => {
    onUpdateSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="flex min-h-screen bg-transparent font-outfit transition-colors duration-500">
      {/* Sidebar */}
      <aside className="w-72 bg-white/5 dark:bg-[#020617]/80 backdrop-blur-2xl border-r border-slate-900/10 dark:border-white/10 flex flex-col sticky top-0 h-screen z-20 animate-fade-in-up">
        <div className="p-8">
          <div className="flex items-center gap-3 mb-10 group cursor-pointer" onClick={() => setCurrentTab('overview')}>
            <div className="h-10 w-10 bg-blue-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-blue-200 group-hover:rotate-12 transition-transform">
              <GraduationCap size={24} />
            </div>
            <h1 className="text-2xl font-black text-slate-900 dark:text-white tracking-tighter">Curio <span className="text-blue-600">AI</span></h1>
          </div>

          <nav className="space-y-2">
            {[
              { id: 'overview', icon: BarChart3, label: 'Analytics' },
              { id: 'reports', icon: FileText, label: 'Session Archive' },
              { id: 'profile', icon: UserIcon, label: 'Instructional Profile' },
              { id: 'settings', icon: Settings, label: 'Configuration' }
            ].map((item) => (
              <button
                key={item.id}
                onClick={() => setCurrentTab(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-black transition-all duration-300 ${
                  currentTab === item.id 
                    ? 'bg-slate-900 dark:bg-blue-600 text-white shadow-xl shadow-slate-200 dark:shadow-blue-900/20 translate-x-1' 
                    : 'text-slate-500 hover:bg-white dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                <item.icon size={18} strokeWidth={currentTab === item.id ? 2.5 : 2} />
                {item.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="mt-auto p-8 space-y-4">
          <div className="p-4 rounded-2xl bg-blue-600/5 dark:bg-blue-600/10 border border-blue-600/10">
            <div className="flex items-center gap-2 text-blue-600 mb-1">
              <Sparkles size={14} />
              <span className="text-[10px] font-black uppercase tracking-widest">Scholar Pro</span>
            </div>
            <p className="text-[10px] text-slate-500 dark:text-slate-400 font-bold leading-relaxed">Upgrade for unlimited teaching sessions and advanced analytics.</p>
          </div>

          <button 
            onClick={() => window.location.reload()}
            className="w-full flex items-center justify-center gap-2 text-rose-600 py-3 rounded-2xl text-[10px] font-black tracking-widest hover:bg-rose-50 dark:hover:bg-rose-900/20 transition-all border border-transparent hover:border-rose-100 dark:hover:border-rose-800"
          >
            <LogOut size={14} />
            LOGOUT
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-6xl mx-auto p-12">
          {currentTab === 'overview' && (
            <div className="space-y-12 animate-fade-in-up">
              {/* Header */}
              <div className="flex items-end justify-between">
                <div>
                  <h2 className="text-4xl font-black text-slate-900 dark:text-white tracking-tighter mb-2">Command Center</h2>
                  <p className="text-slate-500 dark:text-slate-400 font-medium text-sm">System diagnostic and instructional performance overview.</p>
                </div>
                <button 
                  onClick={onBackToLearning}
                  className="group relative flex items-center gap-3 px-10 py-5 rounded-[2.5rem] font-black text-sm transition-all shadow-2xl active:scale-95 tracking-tighter dark:bg-blue-600 dark:text-white dark:shadow-blue-600/30 dark:hover:bg-blue-500 dark:hover:scale-105 bg-slate-900 text-white shadow-slate-900/20 hover:bg-slate-800 hover:scale-105"
                >
                  <Zap size={18} className="fill-current" />
                  START TEACHING
                </button>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-3 gap-8">
                {[
                  { label: 'EVALUATED SESSIONS', value: stats.totalSessions, icon: BrainCircuit, color: 'blue' },
                  { label: 'MASTERY INDEX', value: `${stats.avgScore}%`, icon: TrendingUp, color: 'emerald' },
                  { label: 'PRIMARY DOMAIN', value: stats.topTopic, icon: Star, color: 'amber' }
                ].map((stat, i) => (
                  <div 
                    key={i}
                    className="glass-card bg-white dark:bg-white/5 dark:border dark:border-white/10 rounded-[2.5rem] p-8 relative overflow-hidden group hover:-translate-y-1 transition-all duration-300 shadow-sm backdrop-blur-md"
                  >
                    <div className={`absolute -right-8 -top-8 h-24 w-24 rounded-full ${stat.color === 'blue' ? 'bg-blue-500/5' : stat.color === 'emerald' ? 'bg-emerald-500/5' : 'bg-amber-500/5'} blur-2xl group-hover:scale-150 transition-transform duration-500`}></div>
                    <div className="relative flex items-center gap-5 mb-6">
                      <div className={`h-12 w-12 rounded-2xl ${stat.color === 'blue' ? 'bg-blue-600/10 text-blue-600' : stat.color === 'emerald' ? 'bg-emerald-600/10 text-emerald-600' : 'bg-amber-600/10 text-amber-600'} flex items-center justify-center`}>
                        <stat.icon size={24} />
                      </div>
                      <span className="text-[10px] font-black text-slate-400 tracking-[0.2em] uppercase">{stat.label}</span>
                    </div>
                    <p className="text-3xl font-black text-slate-900 dark:text-white tracking-tight">{stat.value}</p>
                  </div>
                ))}
              </div>

              {/* History Section */}
              <div className="space-y-6">
                <div className="flex items-center justify-between px-2">
                  <h3 className="text-xl font-black text-slate-900 dark:text-white tracking-tight">Analytical Archive</h3>
                  <button 
                    onClick={() => setCurrentTab('reports')}
                    className="text-xs font-black text-blue-600 hover:underline uppercase tracking-widest"
                  >
                    View all reports
                  </button>
                </div>

                {isLoading ? (
                  <div className="grid grid-cols-2 gap-6">
                    {[1, 2, 3, 4].map(i => (
                      <div key={i} className="h-40 rounded-[2.5rem] bg-slate-100/50 dark:bg-slate-800/50 animate-pulse"></div>
                    ))}
                  </div>
                ) : filteredReports.length > 0 ? (
                  <div className="grid grid-cols-2 gap-6">
                    {filteredReports.slice(0, 4).map((report, index) => (
                      <div
                        key={report.report_id || index}
                        onClick={() => onSelectReport(report)}
                        className="glass-card bg-white dark:bg-white/5 dark:border dark:border-white/10 group cursor-pointer p-6 rounded-[2.5rem] flex items-center gap-6 hover:border-blue-200 dark:hover:border-blue-500/50 transition-all duration-300 hover:scale-[1.02] hover:shadow-xl hover:shadow-blue-600/20 active:scale-95 backdrop-blur-md"
                      >
                        <div className="h-20 w-20 rounded-[2rem] bg-slate-900 dark:bg-blue-600 flex flex-col items-center justify-center text-white shrink-0 group-hover:bg-blue-600 dark:group-hover:bg-blue-500 transition-colors shadow-lg">
                          <span className="text-2xl font-black">{report.understanding_score || 0}%</span>
                          <span className="text-[8px] font-bold uppercase tracking-widest opacity-60">Score</span>
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-black text-slate-900 dark:text-white text-lg truncate mb-1">{report.topic}</h4>
                          <div className="flex items-center gap-3 text-slate-400">
                            <div className="flex items-center gap-1">
                              <Clock size={12} />
                              <span className="text-[10px] font-bold uppercase">Recent</span>
                            </div>
                            <div className="h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-700"></div>
                            <span className="text-[10px] font-black text-blue-600 uppercase tracking-widest">{report.mastery_level || 'Scholar'}</span>
                          </div>
                        </div>
                        <div className="h-10 w-10 rounded-full bg-slate-50 dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 dark:group-hover:bg-blue-900/40 group-hover:text-blue-600 transition-all">
                          <ArrowUpRight size={20} />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="py-20 text-center glass-card dark:bg-slate-900/40 rounded-[3rem] border-dashed border-2 dark:border-slate-800">
                    <div className="mx-auto h-16 w-16 bg-slate-100 dark:bg-slate-800 rounded-2xl flex items-center justify-center text-slate-300 mb-4">
                      <FileText size={32} />
                    </div>
                    <p className="text-slate-500 dark:text-slate-400 font-bold">No reports yet. Start your first session!</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {currentTab === 'reports' && (
            <div className="space-y-8 animate-fade-in-up">
              <div className="flex items-center justify-between">
                <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tighter">Learning History</h2>
                <div className="relative w-72">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
                  <input 
                    type="text" 
                    placeholder="Search reports..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-11 pr-4 py-3 bg-white/50 dark:bg-white/5 backdrop-blur-md rounded-[2rem] border border-slate-200 dark:border-white/10 outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-500/20 transition-all font-bold text-sm dark:text-white"
                  />
                </div>
              </div>

              <div className="grid gap-4">
                {isLoading ? (
                  [1,2,3].map(i => <div key={i} className="h-24 rounded-2xl bg-slate-100/50 dark:bg-slate-800/50 animate-pulse"></div>)
                ) : filteredReports.length > 0 ? (
                  filteredReports.map((report, index) => (
                    <div
                      key={report.report_id || index}
                      onClick={() => onSelectReport(report)}
                      className="glass-card bg-white dark:bg-white/5 dark:border dark:border-white/10 group cursor-pointer p-5 rounded-[2rem] flex items-center justify-between hover:border-blue-500 transition-all hover:translate-x-2 active:scale-95 backdrop-blur-md"
                    >
                      <div className="flex items-center gap-6">
                        <div className="h-12 w-12 rounded-xl bg-slate-900 dark:bg-blue-600 text-white flex items-center justify-center font-black shadow-lg group-hover:bg-blue-600 dark:group-hover:bg-blue-500 transition-colors">
                          {report.understanding_score || 0}%
                        </div>
                        <div>
                          <h4 className="font-black text-slate-900 dark:text-white">{report.topic}</h4>
                          <div className="flex items-center gap-3 mt-1">
                            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{report.mastery_level || 'Beginner'}</p>
                            <div className="h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-700"></div>
                            <p className="text-[10px] font-bold text-slate-400">{new Date(report.generated_at).toLocaleDateString()}</p>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <span className="text-[10px] font-black text-blue-600 uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all">Review Insights</span>
                        <ChevronRight className="text-slate-300 dark:text-slate-600 group-hover:text-blue-500 transition-colors" />
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="py-20 text-center glass-card dark:bg-slate-900/40 rounded-[3rem] border-dashed border-2 dark:border-slate-800">
                    <p className="text-slate-500 dark:text-slate-400 font-bold">No reports found matching your search.</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {currentTab === 'settings' && (
            <div className="max-w-3xl mx-auto space-y-8 animate-fade-in-up">
              <div className="flex items-center gap-4 mb-10">
                <div className="h-12 w-12 rounded-2xl bg-slate-900 dark:bg-blue-600 text-white flex items-center justify-center shadow-lg">
                  <Settings size={24} />
                </div>
                <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tighter">Preferences</h2>
              </div>

              <div className="grid gap-6">
                {/* Personality Setting */}
                <div className="glass-card bg-white dark:bg-white/5 dark:border dark:border-white/10 p-8 rounded-[2.5rem] space-y-6 backdrop-blur-md">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-black text-slate-900 dark:text-white">AI Personality</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 font-medium">How should Curio behave during your teaching sessions?</p>
                    </div>
                    <Shield className="text-blue-600" size={24} />
                  </div>
                  <div className="flex flex-wrap gap-3">
                    {["Empathetic student", "Strict evaluator", "Adversarial learner", "Curious child"].map(p => (
                      <button
                        key={p}
                        onClick={() => handleSelectSetting('personality', p)}
                        className={`px-6 py-3 rounded-xl text-xs font-black transition-all ${
                          globalSettings.personality === p 
                          ? 'bg-slate-900 dark:bg-blue-600 text-white shadow-xl shadow-slate-200 dark:shadow-blue-900/40' 
                          : 'bg-slate-50 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-700'
                        }`}
                      >
                        {p}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Toggle Settings */}
                <div className="grid grid-cols-2 gap-6">
                  {[
                    { id: 'voiceEnabled', label: 'Voice Interactions', desc: 'Enable real-time speech responses', icon: Volume2 },
                    { id: 'darkMode', label: 'Dark Mode', desc: 'High-contrast theme for focus', icon: Moon },
                    { id: 'notifications', label: 'Smart Notifications', desc: 'Receive learning gap alerts', icon: Sparkles }
                  ].map(s => (
                    <div key={s.id} className="glass-card bg-white dark:bg-white/5 dark:border dark:border-white/10 p-8 rounded-[2.5rem] flex flex-col justify-between group backdrop-blur-md">
                      <div className="flex items-center justify-between mb-4">
                        <div className="h-10 w-10 rounded-xl bg-slate-50 dark:bg-slate-800 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 dark:group-hover:bg-blue-900/40 group-hover:text-blue-600 transition-all">
                          <s.icon size={20} />
                        </div>
                        <button 
                          onClick={() => handleToggleSetting(s.id)}
                          className={`w-12 h-6 rounded-full relative transition-colors duration-300 ${globalSettings[s.id] ? 'bg-blue-600' : 'bg-slate-200 dark:bg-slate-700'}`}
                        >
                          <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all duration-300 ${globalSettings[s.id] ? 'left-7' : 'left-1'}`}></div>
                        </button>
                      </div>
                      <div>
                        <h4 className="font-black text-slate-900 dark:text-white">{s.label}</h4>
                        <p className="text-xs text-slate-500 dark:text-slate-400 font-medium mt-1">{s.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Save Section */}
                <div className="flex items-center justify-between p-8 bg-slate-900 dark:bg-blue-600 rounded-[2.5rem] text-white shadow-2xl shadow-slate-200 dark:shadow-blue-600/30">
                  <div className="flex items-center gap-4">
                    <Check className="text-emerald-400" size={24} />
                    <p className="font-bold text-sm">Settings are auto-saved to your profile</p>
                  </div>
                  <button 
                    onClick={() => onUpdateSettings({
                      personality: "Empathetic student",
                      difficultyFloor: "Standard",
                      voiceEnabled: true,
                      darkMode: false,
                      notifications: true
                    })}
                    className="px-8 py-3 bg-white text-slate-900 rounded-xl text-xs font-black hover:bg-blue-50 transition-all active:scale-95"
                  >
                    RESET TO DEFAULT
                  </button>
                </div>
              </div>
            </div>
          )}

          {currentTab === 'profile' && (
            <div className="max-w-2xl mx-auto animate-fade-in-up">
              <div className="glass-card bg-white dark:bg-white/5 dark:border dark:border-white/10 backdrop-blur-md rounded-[3rem] p-12 text-center shadow-xl">
                <div className="relative inline-block mb-8">
                  <div className="h-32 w-32 rounded-[2.5rem] bg-gradient-to-br from-blue-500 to-indigo-600 border-8 border-white dark:border-slate-800 shadow-2xl flex items-center justify-center text-white">
                    <UserIcon size={64} />
                  </div>
                  <div className="absolute -bottom-2 -right-2 h-10 w-10 bg-amber-400 rounded-2xl flex items-center justify-center text-white shadow-lg">
                    <Sparkles size={20} />
                  </div>
                </div>
                <h3 className="text-3xl font-black text-slate-900 dark:text-white mb-2">{userEmail.split('@')[0]}</h3>
                <p className="text-blue-600 font-black uppercase tracking-widest text-xs">Master Explainer • Level 12</p>
                
                <div className="grid grid-cols-2 gap-6 mt-12">
                  <div className="bg-slate-50/50 dark:bg-[#020617]/50 p-8 rounded-[2.5rem] border border-slate-100 dark:border-white/10 backdrop-blur-md">
                    <p className="text-3xl font-black text-slate-900 dark:text-white">2,450</p>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Knowledge XP</p>
                  </div>
                  <div className="bg-slate-50/50 dark:bg-[#020617]/50 p-8 rounded-[2.5rem] border border-slate-100 dark:border-white/10 backdrop-blur-md">
                    <p className="text-3xl font-black text-slate-900 dark:text-white">14</p>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">Global Rank</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
