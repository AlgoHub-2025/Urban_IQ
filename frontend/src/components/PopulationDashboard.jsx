import React from 'react';
import { Users, Activity, AlertTriangle, TrendingUp, Bed, UserPlus, ShieldAlert } from 'lucide-react';
import CityMap from './CityMap';

export default function PopulationDashboard({ populationData, hospitals }) {
  // Hardcoded demographic mock data for Hackathon MVP
  const totalPop = 13200000;
  const children = { pct: 35, count: totalPop * 0.35 };
  const working = { pct: 60, count: totalPop * 0.60 };
  const elderly = { pct: 5, count: totalPop * 0.05 };

  const totalHospitals = hospitals?.predictions?.length || 227;
  const totalBeds = totalHospitals * 120; // Avg 120 beds per hospital
  const occupiedBeds = Math.floor(totalBeds * 0.87); // 87% occupancy
  const patientsToday = 11340;
  
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Top Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-slate-900/50 p-5 rounded-2xl border border-white/5">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Total Population</p>
            <Users className="w-5 h-5 text-blue-400" />
          </div>
          <p className="text-3xl font-black text-white">13.2M+</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-blue-500 h-full w-full"></div>
          </div>
          <p className="text-xs text-blue-400 mt-2 flex items-center"><TrendingUp className="w-3 h-3 mr-1"/> High Growth Rate</p>
        </div>

        <div className="bg-slate-900/50 p-5 rounded-2xl border border-white/5">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Children (0-14)</p>
            <p className="text-xs font-bold text-indigo-400">35%</p>
          </div>
          <p className="text-2xl font-bold text-white">4.62M</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-indigo-500 h-full w-[35%]"></div>
          </div>
          <p className="text-xs text-slate-400 mt-2">Pediatric Demand: HIGH</p>
        </div>

        <div className="bg-slate-900/50 p-5 rounded-2xl border border-white/5">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Elderly (65+)</p>
            <p className="text-xs font-bold text-amber-400">5%</p>
          </div>
          <p className="text-2xl font-bold text-white">660K</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-amber-500 h-full w-[5%]"></div>
          </div>
          <p className="text-xs text-slate-400 mt-2">Chronic Care Risk: HIGH</p>
        </div>

        <div className="bg-slate-900/50 p-5 rounded-2xl border border-rose-500/20">
          <div className="flex justify-between items-start mb-2">
            <p className="text-xs font-bold text-rose-500 uppercase tracking-widest">Hospital Load</p>
            <Activity className="w-5 h-5 text-rose-400" />
          </div>
          <p className="text-3xl font-black text-white">87%</p>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-rose-500 h-full w-[87%]"></div>
          </div>
          <p className="text-xs text-rose-400 mt-2 font-bold">⚠ HIGH OCCUPANCY</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Demographics & Healthcare Intel */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-slate-900/50 p-6 rounded-2xl border border-white/5">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6">Patient Load (Today)</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-slate-300">OPD Patients</span><span className="font-bold text-white">8,420</span></div>
                <div className="w-full bg-slate-800 h-2 rounded-full"><div className="bg-emerald-500 h-full rounded-full" style={{width: '75%'}}></div></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-slate-300">Emergency</span><span className="font-bold text-white">2,180</span></div>
                <div className="w-full bg-slate-800 h-2 rounded-full"><div className="bg-amber-500 h-full rounded-full" style={{width: '35%'}}></div></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-slate-300">Admissions</span><span className="font-bold text-white">640</span></div>
                <div className="w-full bg-slate-800 h-2 rounded-full"><div className="bg-blue-500 h-full rounded-full" style={{width: '15%'}}></div></div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1"><span className="text-slate-300">ICU Patients</span><span className="font-bold text-rose-400">120</span></div>
                <div className="w-full bg-slate-800 h-2 rounded-full"><div className="bg-rose-500 h-full rounded-full" style={{width: '8%'}}></div></div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/50 p-6 rounded-2xl border border-white/5">
            <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6 flex items-center">
              <ShieldAlert className="w-4 h-4 mr-2" /> Intelligence Alerts
            </h3>
            <div className="space-y-3">
              <div className="p-3 bg-rose-500/10 border border-rose-500/20 rounded-lg">
                <p className="text-xs font-bold text-rose-400 mb-1">🔴 CRITICAL PRESSURE</p>
                <p className="text-sm text-slate-300">High population + hospital overload detected in Central Lahore.</p>
              </div>
              <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-lg">
                <p className="text-xs font-bold text-amber-400 mb-1">🟠 DEMOGRAPHIC RISK</p>
                <p className="text-sm text-slate-300">Elderly concentration detected in high PM2.5 pollution zones.</p>
              </div>
              <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                <p className="text-xs font-bold text-blue-400 mb-1">ℹ️ PREDICTION MODEL</p>
                <p className="text-sm text-slate-300">Healthcare pressure expected to increase by 8% in the next 24 hours.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Heatmap / Map View */}
        <div className="lg:col-span-2">
          <div className="bg-slate-900/50 p-1 rounded-2xl border border-white/5 h-[650px] relative">
            <div className="absolute top-4 left-4 z-10 bg-slate-900/90 backdrop-blur border border-white/10 p-3 rounded-xl pointer-events-none">
              <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Population & Healthcare Map</p>
              <p className="text-xs text-emerald-400 flex items-center">🟢 Clinics / Hospitals</p>
              <p className="text-xs text-rose-400 flex items-center mt-1">🔴 High-Risk Capacity Zones</p>
            </div>
            {/* Reusing CityMap component for the visual */}
            <CityMap 
              hospitals={hospitals} 
              schools={null} 
              roads={null} 
              showHospitals={true} 
              showSchools={false} 
              showRoads={false} 
            />
          </div>
        </div>
        
      </div>
    </div>
  );
}
