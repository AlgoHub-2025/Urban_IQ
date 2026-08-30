import React from 'react';
import { Wind, Activity } from 'lucide-react';

export default function AQIMode() {
  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      <div className="border-b border-white/10 pb-4">
        <h2 className="text-lg font-bold text-slate-300 tracking-widest uppercase flex items-center">
          <Wind className="w-6 h-6 mr-3 text-rose-400" /> Air Quality Intelligence
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#070b10] p-8 rounded-2xl border border-rose-500/20 relative overflow-hidden">
          <Wind className="absolute right-[-10px] top-[-10px] w-32 h-32 text-rose-500/5" />
          <p className="text-xs font-bold text-rose-500 uppercase tracking-widest mb-2">Current AQI</p>
          <p className="text-7xl font-black text-rose-500">187</p>
          <p className="text-lg font-bold text-white mt-4 flex items-center">
             <Activity className="w-5 h-5 mr-2 text-rose-500" /> UNHEALTHY
          </p>
        </div>

        <div className="md:col-span-2 grid grid-cols-2 gap-4">
          <div className="bg-[#070b10] p-6 rounded-2xl border border-white/5 flex flex-col justify-center">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">PM2.5 Level</span>
            <span className="text-5xl font-black text-rose-400">152 <span className="text-xl">µg/m³</span></span>
            <span className="text-xs text-slate-400 mt-2">Critical threshold exceeded</span>
          </div>
          <div className="bg-[#070b10] p-6 rounded-2xl border border-white/5 flex flex-col justify-center">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">PM10 Level</span>
            <span className="text-5xl font-black text-amber-400">140 <span className="text-xl">µg/m³</span></span>
            <span className="text-xs text-slate-400 mt-2">Elevated particulate matter</span>
          </div>
        </div>
      </div>

      <div className="bg-[#070b10] border border-white/5 rounded-2xl p-6 mt-8">
         <h3 className="text-sm font-bold text-slate-400 tracking-widest uppercase mb-4">Most Affected Sectors</h3>
         <div className="space-y-4">
            <div className="flex justify-between items-center bg-rose-500/10 p-4 rounded-xl border border-rose-500/20">
               <span className="font-bold text-white">Gulberg</span>
               <span className="text-rose-400 font-bold">AQI 195</span>
            </div>
            <div className="flex justify-between items-center bg-rose-500/10 p-4 rounded-xl border border-rose-500/20">
               <span className="font-bold text-white">Johar Town</span>
               <span className="text-rose-400 font-bold">AQI 188</span>
            </div>
            <div className="flex justify-between items-center bg-amber-500/10 p-4 rounded-xl border border-amber-500/20">
               <span className="font-bold text-white">Model Town</span>
               <span className="text-amber-400 font-bold">AQI 172</span>
            </div>
         </div>
      </div>
    </div>
  );
}
