import React from 'react';
import { ShieldAlert, Map, Bell, FileText } from 'lucide-react';

const NAV_ITEMS = [
  { id: 'overview', icon: ShieldAlert, label: 'Overview' },
  { id: 'intelligence', icon: Map, label: 'Intelligence' },
  { id: 'alerts', icon: Bell, label: 'Alerts' },
  { id: 'report', icon: FileText, label: 'Reporting' }
];

export default function Header({ activeTab, setActiveTab }) {
  // Mock current time
  const time = "04:35 PM";
  const date = "30 Aug";

  return (
    <header className="bg-[#0b0f14]/95 backdrop-blur-xl border-b border-white/10 sticky top-0 z-50">
      <div className="max-w-[1600px] mx-auto px-6 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center space-x-3 w-64">
          <div className="w-8 h-8 bg-cyan-500/20 rounded-lg flex items-center justify-center border border-cyan-500/30">
            <ShieldAlert className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h1 className="font-black text-white text-sm tracking-widest leading-none">LAHORE CITY</h1>
            <p className="text-[9px] text-cyan-500 font-bold tracking-[0.2em] mt-1 leading-none">INTELLIGENCE PLATFORM</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="hidden lg:flex items-center space-x-2 flex-1 justify-center">
          {NAV_ITEMS.map(tab => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center px-4 py-2 rounded-lg text-xs font-bold tracking-widest transition-all duration-150 uppercase ${
                  isActive 
                    ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-[0_0_15px_rgba(6,182,212,0.15)]" 
                    : "text-slate-400 hover:text-slate-200 hover:bg-white/5 border border-transparent"
                }`}
              >
                <tab.icon className={`w-4 h-4 mr-2 ${isActive ? 'text-cyan-400' : 'text-slate-500'}`} />
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* System Status */}
        <div className="flex items-center justify-end space-x-4 w-64">
          <div className="text-right hidden md:block">
            <p className="text-xs font-bold text-slate-300">{date} • {time}</p>
          </div>
          <div className="flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full shadow-[0_0_10px_rgba(16,185,129,0.1)]">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
            <span className="text-[9px] font-bold text-emerald-400 tracking-widest uppercase">SYSTEM ONLINE</span>
          </div>
        </div>
      </div>
    </header>
  );
}
