import React, { useState, useEffect } from 'react';
import { GraduationCap, Users, BookOpen, AlertCircle, Search } from 'lucide-react';
import { fetchIntelligence } from '../services/api';

export default function EducationDashboard() {
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIntelligence("Where are the schools?").then(res => {
      setSchools(res.data?.predictions || []);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Top Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5 relative overflow-hidden">
          <GraduationCap className="w-16 h-16 absolute top-0 right-0 opacity-5 text-indigo-500" />
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Total Schools</p>
          <p className="text-4xl font-black text-white">{loading ? '...' : schools.length}</p>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5 relative overflow-hidden">
          <Users className="w-16 h-16 absolute top-0 right-0 opacity-5 text-cyan-500" />
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Est. Enrollment</p>
          <p className="text-4xl font-black text-white">2.8M</p>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Govt vs Private</p>
          <div className="flex items-end mt-2">
            <span className="text-2xl font-black text-indigo-400">42%</span>
            <span className="text-sm font-bold text-slate-500 mx-2">/</span>
            <span className="text-2xl font-black text-cyan-400">58%</span>
          </div>
        </div>
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Student/Teacher Ratio</p>
          <p className="text-4xl font-black text-rose-400">38:1</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Education Demographics Table */}
        <div className="lg:col-span-2 bg-[#0b0f14] border border-white/5 rounded-2xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xs font-bold text-slate-400 tracking-widest uppercase">School Network</h2>
            <div className="relative">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 transform -translate-y-1/2" />
              <input type="text" placeholder="Search schools..." className="bg-black/50 border border-white/10 rounded-lg pl-9 pr-4 py-1.5 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors" />
            </div>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-white/5">
                  <th className="pb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">School Name</th>
                  <th className="pb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Type</th>
                  <th className="pb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Enrollment Status</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr><td colSpan="3" className="text-center py-8 text-slate-500">Loading schools...</td></tr>
                ) : schools.slice(0, 10).map((s, i) => (
                  <tr key={i} className="border-b border-white/5 hover:bg-white/[0.02]">
                    <td className="py-4 text-sm text-white font-bold">{s.name !== 'Unknown' ? s.name : 'Public School'}</td>
                    <td className="py-4 text-sm text-slate-400">{s.predicted_type || 'Education'}</td>
                    <td className="py-4">
                      {i % 4 === 0 ? (
                        <span className="px-2 py-1 bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-bold rounded">AT CAPACITY</span>
                      ) : (
                        <span className="px-2 py-1 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-bold rounded">ACCEPTING</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Education Gaps */}
        <div className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6">
          <h2 className="text-xs font-bold text-amber-500 tracking-widest uppercase mb-4 flex items-center">
             <AlertCircle className="w-4 h-4 mr-2" /> Education Infrastructure Gaps
          </h2>
          <div className="space-y-4">
             <div className="bg-black/50 p-4 rounded-xl border border-white/5">
                <p className="text-sm font-bold text-white mb-1">Ravi Town</p>
                <p className="text-xs text-slate-400">High population density (0-14 bracket) but insufficient government school coverage. Deficit: 12 schools.</p>
             </div>
             <div className="bg-black/50 p-4 rounded-xl border border-white/5">
                <p className="text-sm font-bold text-white mb-1">Wahdat Colony</p>
                <p className="text-xs text-slate-400">Student-to-teacher ratio has exceeded 50:1. Urgent staff deployment required.</p>
             </div>
             <div className="bg-black/50 p-4 rounded-xl border border-white/5">
                <p className="text-sm font-bold text-white mb-1">AQI Hazard Protocol</p>
                <p className="text-xs text-amber-400">14 schools in Gulberg advised to suspend outdoor activities due to PM2.5 levels.</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
