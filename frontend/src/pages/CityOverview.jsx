import React from 'react';
import { Users, Wind, ThermometerSun, HeartPulse, GraduationCap, AlertTriangle, ArrowRight, ShieldAlert, Activity } from 'lucide-react';
import { useAlerts } from '../hooks/useAlerts';

export default function CityOverview({ setActiveTab }) {
  const { alerts } = useAlerts();
  
  // Count active alerts
  const criticalCount = alerts?.filter(a => a.severity === 'critical').length || 0;
  const warningCount = alerts?.filter(a => a.severity === 'warning').length || 0;

  return (
    <div className="space-y-8 max-w-6xl mx-auto animate-in fade-in duration-500">
      
      {/* Hero Briefing */}
      <div className="border-b border-white/10 pb-6 mb-8">
        <h1 className="text-3xl font-black text-white tracking-wide uppercase">Good Afternoon, Lahore</h1>
        <p className="text-slate-400 mt-2 text-lg">City Intelligence Overview — Live status across population, environment & infrastructure.</p>
      </div>

      {/* KPI Grids */}
      <div className="space-y-4">
        {/* Row 1: Operations */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6 relative overflow-hidden">
            <Users className="absolute top-4 right-4 w-12 h-12 text-slate-800" />
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Population</p>
            <p className="text-4xl font-black text-white">13.20M</p>
          </div>
          <div className="bg-[#0b0f14] border border-rose-500/20 rounded-2xl p-6 relative overflow-hidden">
            <Wind className="absolute top-4 right-4 w-12 h-12 text-rose-900/30" />
            <p className="text-xs font-bold text-rose-500 uppercase tracking-widest mb-2">AQI</p>
            <p className="text-4xl font-black text-rose-400">187</p>
            <p className="text-xs font-bold text-rose-500/80 mt-1 uppercase">Unhealthy</p>
          </div>
          <div className="bg-[#0b0f14] border border-amber-500/20 rounded-2xl p-6 relative overflow-hidden">
            <ThermometerSun className="absolute top-4 right-4 w-12 h-12 text-amber-900/30" />
            <p className="text-xs font-bold text-amber-500 uppercase tracking-widest mb-2">Weather</p>
            <p className="text-4xl font-black text-amber-400">36°C</p>
          </div>
          <div className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6 relative overflow-hidden">
            <HeartPulse className="absolute top-4 right-4 w-12 h-12 text-slate-800" />
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Hospital Occupancy</p>
            <p className="text-4xl font-black text-white">78%</p>
          </div>
        </div>

        {/* Row 2: Demographics & Assets */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-4">
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Children (0-14)</p>
            <p className="text-2xl font-black text-white">3.28M</p>
          </div>
          <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-4">
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Elderly (65+)</p>
            <p className="text-2xl font-black text-white">1.14M</p>
          </div>
          <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-4">
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Schools</p>
            <p className="text-2xl font-black text-white">1,763</p>
          </div>
          <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-4 cursor-pointer hover:bg-white/[0.05]" onClick={() => setActiveTab('alerts')}>
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Active Alerts</p>
            <p className="text-2xl font-black text-white">{alerts?.length || 0}</p>
          </div>
        </div>
      </div>

      {/* Modular Panels */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* City Health */}
        <div className="bg-[#0b0f14] border border-white/5 rounded-3xl p-8">
          <h2 className="text-sm font-bold text-slate-300 tracking-widest uppercase mb-6 flex items-center">
            <HeartPulse className="w-5 h-5 mr-3 text-emerald-500" /> City Health
          </h2>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between text-sm font-bold mb-2">
                <span className="text-slate-400">Hospital Occupancy</span>
                <span className="text-white">78%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-500 h-full" style={{ width: '78%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm font-bold mb-2">
                <span className="text-slate-400">Patients Today</span>
                <span className="text-white">8,420</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-cyan-500 h-full" style={{ width: '65%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Environment */}
        <div className="bg-[#0b0f14] border border-white/5 rounded-3xl p-8">
          <h2 className="text-sm font-bold text-slate-300 tracking-widest uppercase mb-6 flex items-center">
            <Wind className="w-5 h-5 mr-3 text-cyan-500" /> Environment
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-sm font-bold text-slate-400">AQI Trend</span>
              <span className="text-sm font-black text-rose-400 flex items-center">187 <Activity className="w-4 h-4 ml-2" /></span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-sm font-bold text-slate-400">PM2.5 Level</span>
              <span className="text-sm font-black text-rose-400">152 µg/m³</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-sm font-bold text-slate-400">Temperature</span>
              <span className="text-sm font-black text-amber-400">36°C</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-sm font-bold text-slate-400">Weather Risk</span>
              <span className="text-sm font-black text-amber-400">ELEVATED</span>
            </div>
          </div>
        </div>

        {/* Demographics */}
        <div className="bg-[#0b0f14] border border-white/5 rounded-3xl p-8">
          <h2 className="text-sm font-bold text-slate-300 tracking-widest uppercase mb-6 flex items-center">
            <Users className="w-5 h-5 mr-3 text-indigo-500" /> Demographics
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-sm font-bold text-slate-400">Children</span>
              <span className="text-sm font-black text-white">3.28M</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-sm font-bold text-slate-400">Working Age</span>
              <span className="text-sm font-black text-white">8.78M</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-white/5">
              <span className="text-sm font-bold text-slate-400">Elderly</span>
              <span className="text-sm font-black text-white">1.14M</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-sm font-bold text-rose-500">Vulnerable Population Exposed</span>
              <span className="text-sm font-black text-rose-400">4.42M</span>
            </div>
          </div>
        </div>

        {/* Active Alerts */}
        <div className="bg-[#0b0f14] border border-rose-500/10 rounded-3xl p-8">
          <h2 className="text-sm font-bold text-rose-500 tracking-widest uppercase mb-6 flex items-center">
            <AlertTriangle className="w-5 h-5 mr-3 text-rose-500 animate-pulse" /> Active System Alerts
          </h2>
          <div className="space-y-3">
            {(alerts || []).slice(0, 4).map((a, i) => (
              <div key={i} className="flex items-center space-x-3 bg-white/5 p-3 rounded-lg border border-white/5">
                <span className={`w-3 h-3 rounded-full ${a.severity === 'critical' ? 'bg-rose-500' : a.severity === 'warning' ? 'bg-amber-500' : 'bg-blue-500'}`}></span>
                <span className="text-sm font-bold text-white truncate">{a.title}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Map CTA */}
      <div 
        onClick={() => setActiveTab('intelligence')}
        className="mt-12 bg-gradient-to-r from-cyan-900/40 to-blue-900/40 border border-cyan-500/30 rounded-2xl p-8 flex items-center justify-between cursor-pointer hover:from-cyan-900/60 hover:to-blue-900/60 transition-all group"
      >
        <div>
          <h2 className="text-2xl font-black text-white tracking-widest uppercase">Explore Lahore on the Intelligence Map</h2>
          <p className="text-cyan-400 mt-2 font-medium">Switch to spatial analysis workspace to investigate active alerts and city infrastructure.</p>
        </div>
        <div className="w-12 h-12 rounded-full bg-cyan-500/20 flex items-center justify-center group-hover:bg-cyan-500/40 transition-colors">
          <ArrowRight className="w-6 h-6 text-cyan-400" />
        </div>
      </div>

    </div>
  );
}
