import React, { useState, useEffect } from 'react';
import { GraduationCap } from 'lucide-react';
import { fetchSchools } from '../../services/api';

export default function EducationMode() {
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSchools().then(res => {
      setSchools(res?.predictions || []);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="border-b border-white/10 pb-4">
        <h2 className="text-sm font-bold text-slate-300 tracking-widest uppercase flex items-center">
          <GraduationCap className="w-4 h-4 mr-2 text-indigo-400" /> Education Intelligence
        </h2>
      </div>

      <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
        <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Total Schools</p>
        <p className="text-3xl font-black text-white">{loading ? '...' : schools.length}</p>
      </div>

      <div className="space-y-3">
        <div className="bg-black/40 p-4 rounded-xl border border-white/5 flex justify-between items-center">
          <span className="text-xs font-bold text-slate-400">Total Enrollment</span>
          <span className="text-sm font-black text-white">2.8M</span>
        </div>
        <div className="bg-black/40 p-4 rounded-xl border border-white/5 flex justify-between items-center">
          <span className="text-xs font-bold text-slate-400">Govt / Private</span>
          <span className="text-sm font-black text-white">42% / 58%</span>
        </div>
        <div className="bg-black/40 p-4 rounded-xl border border-amber-500/20 flex justify-between items-center">
          <span className="text-xs font-bold text-amber-500">Student/Teacher Ratio</span>
          <span className="text-sm font-black text-amber-400">38:1</span>
        </div>
      </div>
    </div>
  );
}
