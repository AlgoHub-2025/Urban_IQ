import React, { useState, useEffect } from 'react';
import CityMap from '../components/CityMap';
import { fetchIntelligence } from '../services/api';
import { Layers, Activity, Users, GraduationCap, Navigation } from 'lucide-react';

export default function InteractiveMapPage() {
  const [hospitals, setHospitals] = useState(null);
  const [schools, setSchools] = useState(null);
  const [roads, setRoads] = useState(null);

  const [layers, setLayers] = useState({
    hospitals: true,
    schools: false,
    roads: false
  });

  useEffect(() => {
    // Fetch map data on mount
    fetchIntelligence("Where are the hospitals?").then(res => setHospitals(res.data));
    fetchIntelligence("Where are the schools?").then(res => setSchools(res.data));
    fetchIntelligence("Show me the roads").then(res => setRoads(res.data));
  }, []);

  const toggleLayer = (key) => setLayers(prev => ({ ...prev, [key]: !prev[key] }));

  return (
    <div className="relative h-[calc(100vh-140px)] w-full bg-[#0b0f14] border border-white/5 rounded-2xl overflow-hidden shadow-2xl">
      
      {/* Floating Map Layer Controls */}
      <div className="absolute top-6 left-6 z-[400] bg-[#070b10]/90 backdrop-blur-md border border-white/10 rounded-xl p-4 shadow-2xl min-w-[200px]">
        <h3 className="text-xs font-bold text-slate-400 tracking-widest uppercase mb-4 flex items-center">
          <Layers className="w-4 h-4 mr-2" /> Map Layers
        </h3>
        
        <div className="space-y-3">
          <label className="flex items-center space-x-3 cursor-pointer group" onClick={() => toggleLayer('hospitals')}>
            <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${layers.hospitals ? 'bg-rose-500 border-rose-500' : 'border-slate-600 group-hover:border-slate-400'}`}>
              {layers.hospitals && <Activity className="w-3 h-3 text-white" />}
            </div>
            <span className={`text-sm font-bold ${layers.hospitals ? 'text-white' : 'text-slate-400'}`}>Hospitals</span>
          </label>
          
          <label className="flex items-center space-x-3 cursor-pointer group" onClick={() => toggleLayer('schools')}>
            <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${layers.schools ? 'bg-indigo-500 border-indigo-500' : 'border-slate-600 group-hover:border-slate-400'}`}>
              {layers.schools && <GraduationCap className="w-3 h-3 text-white" />}
            </div>
            <span className={`text-sm font-bold ${layers.schools ? 'text-white' : 'text-slate-400'}`}>Schools</span>
          </label>

          <label className="flex items-center space-x-3 cursor-pointer group" onClick={() => toggleLayer('roads')}>
            <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${layers.roads ? 'bg-slate-400 border-slate-400' : 'border-slate-600 group-hover:border-slate-400'}`}>
              {layers.roads && <Navigation className="w-3 h-3 text-[#070b10]" />}
            </div>
            <span className={`text-sm font-bold ${layers.roads ? 'text-white' : 'text-slate-400'}`}>Road Infrastructure</span>
          </label>
        </div>
      </div>

      <div className="absolute top-6 right-6 z-[400]">
         <div className="bg-[#070b10]/90 backdrop-blur-md border border-white/10 rounded-xl p-4 shadow-2xl">
            <h3 className="text-xs font-bold text-slate-400 tracking-widest uppercase mb-3">Legend</h3>
            <div className="space-y-2">
              <div className="flex items-center text-xs text-slate-300"><span className="w-3 h-3 rounded-full bg-emerald-500 mr-2"></span> Safe / Normal Capacity</div>
              <div className="flex items-center text-xs text-slate-300"><span className="w-3 h-3 rounded-full bg-yellow-500 mr-2"></span> Warning / Elevated</div>
              <div className="flex items-center text-xs text-slate-300"><span className="w-3 h-3 rounded-full bg-rose-500 mr-2"></span> Critical / Over Capacity</div>
            </div>
         </div>
      </div>

      {/* Main Map */}
      <div className="w-full h-full">
        <CityMap 
          hospitals={hospitals} 
          schools={schools} 
          roads={roads}
          showHospitals={layers.hospitals}
          showSchools={layers.schools}
          showRoads={layers.roads}
        />
      </div>

    </div>
  );
}
