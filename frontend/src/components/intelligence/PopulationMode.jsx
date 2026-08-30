import React from 'react';
import { Users, Activity } from 'lucide-react';

export default function PopulationMode() {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="border-b border-white/10 pb-4">
        <h2 className="text-sm font-bold text-slate-300 tracking-widest uppercase flex items-center">
          <Users className="w-4 h-4 mr-2 text-indigo-400" /> Population Intelligence
        </h2>
      </div>

      <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Total Population</p>
        <p className="text-3xl font-black text-white">13.20M</p>
      </div>

      <div className="space-y-3">
        <div className="bg-black/40 p-4 rounded-xl border border-white/5 flex justify-between items-center">
          <span className="text-xs font-bold text-slate-400">Children (0-14)</span>
          <span className="text-sm font-black text-white">24.8%</span>
        </div>
        <div className="bg-black/40 p-4 rounded-xl border border-white/5 flex justify-between items-center">
          <span className="text-xs font-bold text-slate-400">Working Age</span>
          <span className="text-sm font-black text-emerald-400">66.5%</span>
        </div>
        <div className="bg-black/40 p-4 rounded-xl border border-white/5 flex justify-between items-center">
          <span className="text-xs font-bold text-slate-400">Elderly (65+)</span>
          <span className="text-sm font-black text-rose-400">8.7%</span>
        </div>
      </div>

      <div className="bg-black/40 p-5 rounded-2xl border border-white/5">
        <h3 className="text-xs font-bold text-slate-500 tracking-widest uppercase mb-4">Density Hotspots</h3>
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-white">Central Lahore</span>
            <span className="text-[10px] font-bold bg-amber-500/10 text-amber-500 px-2 py-1 rounded">HIGH</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-white">Gulberg</span>
            <span className="text-[10px] font-bold bg-amber-500/10 text-amber-500 px-2 py-1 rounded">HIGH</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-sm font-bold text-white">Ravi Town</span>
            <span className="text-[10px] font-bold bg-rose-500/10 text-rose-500 px-2 py-1 rounded">VERY HIGH</span>
          </div>
        </div>
      </div>
    </div>
  );
}
