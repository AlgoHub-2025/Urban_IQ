import React, { useState, useEffect } from 'react';
import { HeartPulse, Bed, AlertTriangle, Search, Activity, UserPlus } from 'lucide-react';
import { fetchIntelligence } from '../services/api';

export default function HealthcareDashboard() {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIntelligence("Where are the hospitals?").then(res => {
      setHospitals(res.data?.predictions || []);
      setLoading(false);
    });
  }, []);

  const totalBeds = hospitals.length * 120; // Mock 120 beds average
  const occupiedBeds = Math.floor(totalBeds * 0.92);
  const occupancyRate = 92;

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Top Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Total Hospitals</p>
          <p className="text-4xl font-black text-white">{loading ? '...' : hospitals.length}</p>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5 relative overflow-hidden">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Occupancy Rate</p>
          <p className="text-4xl font-black text-rose-500">{occupancyRate}%</p>
          <div className="absolute bottom-0 left-0 h-1 bg-rose-500" style={{ width: '92%' }}></div>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Available Beds</p>
          <p className="text-4xl font-black text-amber-500">{loading ? '...' : totalBeds - occupiedBeds}</p>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Patients Today</p>
          <p className="text-4xl font-black text-white">14,203</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Hospital Operations Table */}
        <div className="lg:col-span-2 bg-[#0b0f14] border border-white/5 rounded-2xl p-6 flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xs font-bold text-slate-400 tracking-widest uppercase">Hospital Operations</h2>
            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 transform -translate-y-1/2" />
              <input type="text" placeholder="Search hospitals..." className="bg-black/50 border border-white/10 rounded-lg pl-9 pr-4 py-1.5 text-sm text-white focus:outline-none focus:border-cyan-500 transition-colors" />
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/5">
                  <th className="pb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Facility Name</th>
                  <th className="pb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Type</th>
                  <th className="pb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Status</th>
                  <th className="pb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Beds</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan="4" className="text-center py-8 text-slate-500">Loading hospitals...</td></tr>
                ) : hospitals.slice(0, 10).map((h, i) => (
                  <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02]">
                    <td className="py-4 text-sm text-white font-bold">{h.name !== 'Unknown' ? h.name : 'General Hospital'}</td>
                    <td className="py-4 text-sm text-slate-400">{h.predicted_type || 'Healthcare'}</td>
                    <td className="py-4">
                      {i % 3 === 0 ? (
                        <span className="px-2 py-1 bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-bold rounded">OVER CAPACITY</span>
                      ) : (
                        <span className="px-2 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-bold rounded">NORMAL</span>
                      )}
                    </td>
                    <td className="py-4 text-sm text-slate-300">{(120 - (i*5))} / 120</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Live Triage Alerts */}
        <div className="bg-[#0b0f14] border border-rose-500/10 rounded-2xl p-6">
          <h2 className="text-xs font-bold text-rose-500 tracking-widest uppercase mb-4 flex items-center">
             <AlertTriangle className="w-4 h-4 mr-2" /> Live Triage Alerts
          </h2>
          <div className="space-y-4">
             <div className="bg-rose-500/10 p-4 rounded-xl border border-rose-500/20">
                <p className="text-sm font-bold text-white mb-1">Services Hospital</p>
                <p className="text-xs text-rose-400">ER at 115% capacity. Divert inbound trauma patients to Mayo Hospital immediately.</p>
             </div>
             <div className="bg-amber-500/10 p-4 rounded-xl border border-amber-500/20">
                <p className="text-sm font-bold text-white mb-1">Jinnah Hospital</p>
                <p className="text-xs text-amber-400">Ventilator availability critically low (2 remaining). Requesting emergency logistics.</p>
             </div>
             <div className="bg-white/5 p-4 rounded-xl border border-white/10">
                <p className="text-sm font-bold text-white mb-1">Overall Network</p>
                <p className="text-xs text-slate-400">Heatwave protocol active. OPD respiratory cases up 18% since yesterday.</p>
             </div>
          </div>
        </div>
      </div>

    </div>
  );
}
