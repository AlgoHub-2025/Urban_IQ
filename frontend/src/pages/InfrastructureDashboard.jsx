import React, { useState, useEffect } from 'react';
import { Navigation, Car, AlertOctagon, Activity, Map } from 'lucide-react';
import { fetchIntelligence } from '../services/api';

export default function InfrastructureDashboard() {
  const [roads, setRoads] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIntelligence("Show me the roads").then(res => {
      setRoads(res.data?.predictions || []);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Top Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5 relative overflow-hidden">
          <Navigation className="w-16 h-16 absolute top-0 right-0 opacity-5 text-slate-400" />
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Tracked Segments</p>
          <p className="text-4xl font-black text-white">{loading ? '...' : roads.length}</p>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5 relative overflow-hidden">
          <Car className="w-16 h-16 absolute top-0 right-0 opacity-5 text-amber-500" />
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Traffic Congestion</p>
          <p className="text-4xl font-black text-amber-500">Severe</p>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5 relative overflow-hidden">
          <AlertOctagon className="w-16 h-16 absolute top-0 right-0 opacity-5 text-rose-500" />
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Active Incidents</p>
          <p className="text-4xl font-black text-rose-400">14</p>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-emerald-500/10">
          <p className="text-xs font-bold text-emerald-500 uppercase tracking-widest mb-1">Network Status</p>
          <p className="text-2xl font-black text-emerald-400 mt-2 flex items-center">
             <Activity className="w-5 h-5 mr-2 animate-pulse" /> OPERATIONAL
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Ranked Problematic Roads */}
        <div className="lg:col-span-2 bg-[#0b0f14] border border-white/5 rounded-2xl p-6">
          <h2 className="text-xs font-bold text-slate-400 tracking-widest uppercase mb-6">High-Risk Infrastructure Segments</h2>
          
          <div className="space-y-3">
             {[
               { name: 'Canal Bank Road (FC College)', risk: 'Critical', issue: 'Potholes & Flooding Risk', time: '14 mins delay' },
               { name: 'Ferozepur Road (Kalma Chowk)', risk: 'High', issue: 'Traffic Bottleneck', time: '22 mins delay' },
               { name: 'Multan Road (Thokar Niaz Baig)', risk: 'High', issue: 'Heavy Freight Congestion', time: '18 mins delay' },
               { name: 'Mall Road (GPO Chowk)', risk: 'Moderate', issue: 'Protest Diversion', time: '8 mins delay' },
               { name: 'Jail Road', risk: 'Moderate', issue: 'Signal Outage', time: '5 mins delay' },
             ].map((road, i) => (
               <div key={i} className="flex items-center justify-between p-4 bg-black/50 border border-white/5 rounded-xl hover:bg-white/[0.02] transition-colors">
                  <div className="flex items-center space-x-4">
                     <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                        <span className="text-xs font-bold text-slate-400">#{i+1}</span>
                     </div>
                     <div>
                        <p className="font-bold text-white text-sm">{road.name}</p>
                        <p className="text-xs text-slate-500 mt-1">{road.issue}</p>
                     </div>
                  </div>
                  <div className="text-right">
                     <p className={`text-xs font-bold px-2 py-1 rounded inline-block ${road.risk === 'Critical' ? 'bg-rose-500/10 text-rose-400' : road.risk === 'High' ? 'bg-amber-500/10 text-amber-400' : 'bg-yellow-500/10 text-yellow-400'}`}>
                       {road.risk}
                     </p>
                     <p className="text-xs text-slate-400 mt-2">{road.time}</p>
                  </div>
               </div>
             ))}
          </div>
        </div>

        {/* Infrastructure AI Analysis */}
        <div className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6">
          <h2 className="text-xs font-bold text-cyan-500 tracking-widest uppercase mb-4 flex items-center">
             <Map className="w-4 h-4 mr-2" /> Predictive Analysis
          </h2>
          <div className="prose prose-invert prose-sm">
             <p className="text-slate-400">The ML model predicts a <strong>24% increase</strong> in traffic congestion on major arteries connecting to Gulberg during the 5PM-7PM window.</p>
             <p className="text-slate-400">Monsoon weather forecasts indicate high probability of urban flooding along Canal Road underpasses.</p>
             <div className="mt-6 p-4 bg-cyan-500/10 border border-cyan-500/20 rounded-xl">
                <p className="text-cyan-400 font-bold text-sm">Action Recommended</p>
                <p className="text-cyan-500/70 text-xs mt-1">Deploy mobile pumping stations to Underpass 4 & 5. Reroute heavy freight from Ferozepur Road.</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
