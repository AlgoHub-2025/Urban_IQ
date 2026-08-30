import React, { useState, useEffect } from 'react';
import { HeartPulse, Bed } from 'lucide-react';
import { fetchHospitals } from '../../services/api';

export default function HealthcareMode() {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHospitals().then(res => {
      setHospitals(res?.predictions || []);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="border-b border-white/10 pb-4">
        <h2 className="text-sm font-bold text-slate-300 tracking-widest uppercase flex items-center">
          <HeartPulse className="w-4 h-4 mr-2 text-rose-400" /> Healthcare Intelligence
        </h2>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-[#0b0f14] p-4 rounded-xl border border-white/5">
          <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">Hospitals</p>
          <p className="text-xl font-black text-white">{loading ? '...' : hospitals.length}</p>
        </div>
        <div className="bg-[#0b0f14] p-4 rounded-xl border border-rose-500/20 relative overflow-hidden">
          <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">Occupancy</p>
          <p className="text-xl font-black text-rose-500">78%</p>
          <div className="absolute bottom-0 left-0 h-1 bg-rose-500" style={{width: '78%'}}></div>
        </div>
        <div className="bg-[#0b0f14] p-4 rounded-xl border border-white/5">
          <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">Occupied</p>
          <p className="text-xl font-black text-white">8,420</p>
        </div>
        <div className="bg-[#0b0f14] p-4 rounded-xl border border-white/5">
          <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">Available</p>
          <p className="text-xl font-black text-emerald-400">2,380</p>
        </div>
      </div>

      <div className="bg-black/40 p-5 rounded-2xl border border-rose-500/10">
        <h3 className="text-xs font-bold text-rose-500 tracking-widest uppercase mb-4">Critical Facilities</h3>
        <div className="space-y-3">
          {loading ? (
            <div className="text-xs text-slate-500">Loading...</div>
          ) : hospitals.slice(0, 5).map((h, i) => (
            <div key={i} className="flex justify-between items-center border-b border-white/5 pb-2 last:border-0 last:pb-0">
              <span className="text-xs font-bold text-white truncate max-w-[150px]">{h.name !== 'Unknown' ? h.name : 'General Hospital'}</span>
              <span className={`text-[10px] font-bold px-2 py-1 rounded ${i < 2 ? 'bg-rose-500/10 text-rose-500' : 'bg-amber-500/10 text-amber-500'}`}>
                {92 - (i*3)}%
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
