import React from 'react';
import { Users, Activity, TrendingUp, AlertTriangle } from 'lucide-react';

export default function PopulationDashboard() {
  const totalPop = 13200000;
  const children = { pct: 35, count: totalPop * 0.35 };
  const working = { pct: 60, count: totalPop * 0.60 };
  const elderly = { pct: 5, count: totalPop * 0.05 };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Top Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Total Population</p>
            <Users className="w-5 h-5 text-blue-400" />
          </div>
          <p className="text-3xl font-black text-white">13.2M+</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-blue-500 h-full w-full"></div>
          </div>
        </div>

        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Children (0-14)</p>
            <div className="text-xs font-bold text-blue-400 bg-blue-500/10 px-2 py-1 rounded">35%</div>
          </div>
          <p className="text-3xl font-black text-white">4.62M</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-blue-400 h-full" style={{width: '35%'}}></div>
          </div>
        </div>

        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Working (15-64)</p>
            <div className="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded">60%</div>
          </div>
          <p className="text-3xl font-black text-white">7.92M</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full" style={{width: '60%'}}></div>
          </div>
        </div>

        <div className="bg-[#0b0f14] p-5 rounded-2xl border border-white/5">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Elderly (65+)</p>
            <div className="text-xs font-bold text-rose-400 bg-rose-500/10 px-2 py-1 rounded">5%</div>
          </div>
          <p className="text-3xl font-black text-white">0.66M</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-rose-500 h-full" style={{width: '5%'}}></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
         {/* Density Map Placeholder */}
         <div className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6 h-[400px] flex flex-col items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 opacity-20 bg-[url('https://cartodb-basemaps-c.global.ssl.fastly.net/dark_all/12/2884/1666.png')] bg-cover bg-center filter grayscale"></div>
            <Activity className="w-12 h-12 text-slate-500 mb-4 animate-pulse relative z-10" />
            <h3 className="text-slate-300 font-bold tracking-widest uppercase relative z-10">Population Density Heatmap</h3>
            <p className="text-slate-500 text-sm mt-2 relative z-10">Integration Pending</p>
         </div>

         {/* Vulnerability Analysis */}
         <div className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6">
            <h3 className="text-xs font-bold text-rose-500 tracking-widest uppercase mb-6 flex items-center">
              <AlertTriangle className="w-4 h-4 mr-2" /> Vulnerability Intelligence
            </h3>
            
            <div className="space-y-4">
              <div className="bg-black/50 rounded-xl p-4 border border-rose-500/20">
                <div className="flex justify-between">
                  <p className="text-slate-300 font-bold">Walled City District</p>
                  <p className="text-rose-400 font-bold">Critical</p>
                </div>
                <p className="text-xs text-slate-500 mt-1">Extreme population density overlapping with AQI > 150. Elderly population (12%) highly vulnerable.</p>
              </div>
              <div className="bg-black/50 rounded-xl p-4 border border-amber-500/20">
                <div className="flex justify-between">
                  <p className="text-slate-300 font-bold">Gulberg District</p>
                  <p className="text-amber-400 font-bold">Elevated</p>
                </div>
                <p className="text-xs text-slate-500 mt-1">High working-class movement during peak traffic hours. Respiratory exposure increased.</p>
              </div>
              <div className="bg-black/50 rounded-xl p-4 border border-white/5">
                <div className="flex justify-between">
                  <p className="text-slate-300 font-bold">DHA Phase 6</p>
                  <p className="text-emerald-400 font-bold">Nominal</p>
                </div>
                <p className="text-xs text-slate-500 mt-1">Low density, high green cover. Vulnerability metrics within safe parameters.</p>
              </div>
            </div>
         </div>
      </div>
    </div>
  );
}
