import React, { useState, useEffect } from 'react';
import { Users, CloudRain, HeartPulse, GraduationCap, Wind, AlertTriangle } from 'lucide-react';
import CityMap from '../components/CityMap';
import { fetchHospitals, fetchSchools } from '../services/api';

// Modes
import PopulationMode from '../components/intelligence/PopulationMode';
import HealthcareMode from '../components/intelligence/HealthcareMode';
import EducationMode from '../components/intelligence/EducationMode';
import WeatherMode from '../components/intelligence/WeatherMode';
import AQIMode from '../components/intelligence/AQIMode';

const MODES = [
  { id: 'population', label: 'Population', icon: Users },
  { id: 'healthcare', label: 'Healthcare', icon: HeartPulse },
  { id: 'education', label: 'Education', icon: GraduationCap },
  { id: 'weather', label: 'Weather', icon: CloudRain },
  { id: 'aqi', label: 'Air Quality', icon: Wind },
  { id: 'risk', label: 'Risk Zones', icon: AlertTriangle }
];

export default function CityIntelligenceExplorer() {
  const [activeMode, setActiveMode] = useState('population');
  const [hospitals, setHospitals] = useState(null);
  const [schools, setSchools] = useState(null);

  useEffect(() => {
    // Fetch all map data once
    fetchHospitals().then(res => setHospitals(res));
    fetchSchools().then(res => setSchools(res));
  }, []);

  const renderContextPanel = () => {
    switch(activeMode) {
      case 'population': return <PopulationMode />;
      case 'healthcare': return <HealthcareMode />;
      case 'education': return <EducationMode />;
      case 'weather': return <WeatherMode />;
      case 'aqi': return <AQIMode />;
      case 'risk': return <div className="p-4 text-center text-rose-500">Risk Zones mapping...</div>;
      default: return <PopulationMode />;
    }
  };

  const showMap = activeMode !== 'weather' && activeMode !== 'aqi';

  return (
    <div className="flex flex-col lg:flex-row gap-6 h-[calc(100vh-140px)] w-full animate-in fade-in duration-500">
      
      {/* Sidebar: Intelligence Modes */}
      <div className="w-full lg:w-64 flex-shrink-0 bg-[#0b0f14] border border-white/5 rounded-2xl p-4 flex flex-col">
        <h3 className="text-xs font-bold text-slate-500 tracking-widest uppercase mb-4 px-2">Intelligence Modes</h3>
        <div className="space-y-1 overflow-y-auto pr-2">
          {MODES.map(mode => (
            <button
              key={mode.id}
              onClick={() => setActiveMode(mode.id)}
              className={`w-full flex items-center px-4 py-3 rounded-xl text-sm font-bold transition-all ${
                activeMode === mode.id 
                  ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5 border border-transparent'
              }`}
            >
              <mode.icon className={`w-4 h-4 mr-3 ${activeMode === mode.id ? 'text-cyan-400' : 'text-slate-500'}`} />
              {mode.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Canvas: ONE MAP (Conditionally Rendered) */}
      {showMap && (
        <div className="flex-1 h-full bg-[#0b0f14] border border-white/5 rounded-2xl overflow-hidden relative">
          <CityMap 
            hospitals={hospitals} 
            schools={schools} 
            roads={null}
            // The map layers react dynamically to the active mode!
            showHospitals={activeMode === 'healthcare' || activeMode === 'risk'}
            showSchools={activeMode === 'education' || activeMode === 'risk'}
            showRoads={false}
          />
          
          {/* Map Label Overlay */}
          <div className="absolute top-4 left-4 z-[400] pointer-events-none">
            <div className="bg-black/80 backdrop-blur-md border border-white/10 px-4 py-2 rounded-lg">
               <span className="text-xs font-bold text-white tracking-widest uppercase flex items-center">
                  <span className="w-2 h-2 rounded-full bg-cyan-500 mr-2 animate-pulse"></span>
                  Lahore {MODES.find(m => m.id === activeMode)?.label} Map
               </span>
            </div>
          </div>
        </div>
      )}

      {/* Context Panel */}
      <div className={`${showMap ? 'w-full lg:w-80 flex-shrink-0' : 'flex-1'} bg-[#0b0f14] border border-white/5 rounded-2xl p-6 overflow-y-auto`}>
        {renderContextPanel()}
      </div>

    </div>
  );
}
