import React, { useState, useEffect } from 'react';
import CityMap from '../components/CityMap';
import { fetchHospitals, fetchSchools, fetchRoads, fetchZones } from '../services/api';
import { Layers, Activity, Users, GraduationCap, Navigation, Map } from 'lucide-react';
import WhyThisRiskPanel from '../components/intelligence/WhyThisRiskPanel';
import EmergencyResourcesPanel from '../components/intelligence/EmergencyResourcesPanel';
import ResponseTwinPanel from '../components/intelligence/ResponseTwinPanel';

export default function InteractiveMapPage() {
  const [hospitals, setHospitals] = useState(null);
  const [schools, setSchools] = useState(null);
  const [roads, setRoads] = useState(null);
  const [zones, setZones] = useState(null);
  const [selectedZone, setSelectedZone] = useState(null);
  const [reports, setReports] = useState([]);

  const [layers, setLayers] = useState({
    zones: true,
    hospitals: true,
    schools: false,
    roads: true,
    reports: true
  });

  useEffect(() => {
    fetchHospitals().then(setHospitals).catch(console.error);
    fetchSchools().then(setSchools).catch(console.error);
    fetchRoads().then(setRoads).catch(console.error);
    fetchZones().then(setZones).catch(console.error);
    fetch('http://localhost:8009/api/reports')
      .then(res => res.json())
      .then(data => setReports(data.reports.filter(r => r.status === 'verified')))
      .catch(console.error);
  }, []);

  const toggleLayer = (key) => setLayers(prev => ({ ...prev, [key]: !prev[key] }));

  return (
    <div className="relative h-[calc(100vh-140px)] w-full bg-[#0b0f14] border border-white/5 rounded-2xl overflow-hidden shadow-2xl flex">
      
      {/* Floating Map Layer Controls */}
      <div className="absolute top-6 left-6 z-[400] bg-[#070b10]/90 backdrop-blur-md border border-white/10 rounded-xl p-4 shadow-2xl min-w-[200px]">
        <h3 className="text-xs font-bold text-slate-400 tracking-widest uppercase mb-4 flex items-center">
          <Layers className="w-4 h-4 mr-2" /> Map Layers
        </h3>
        
        <div className="space-y-3">
          <label className="flex items-center space-x-3 cursor-pointer group" onClick={() => toggleLayer('zones')}>
            <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${layers.zones ? 'bg-amber-500 border-amber-500' : 'border-slate-600 group-hover:border-slate-400'}`}>
              {layers.zones && <Map className="w-3 h-3 text-white" />}
            </div>
            <span className={`text-sm font-bold ${layers.zones ? 'text-white' : 'text-slate-400'}`}>Risk Zones</span>
          </label>
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
            <span className={`text-sm font-bold ${layers.roads ? 'text-white' : 'text-slate-400'}`}>Roads</span>
          </label>

          <label className="flex items-center space-x-3 cursor-pointer group mt-4 pt-4 border-t border-white/10" onClick={() => toggleLayer('reports')}>
            <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${layers.reports ? 'bg-cyan-500 border-cyan-500' : 'border-slate-600 group-hover:border-slate-400'}`}>
              {layers.reports && <Users className="w-3 h-3 text-[#070b10]" />}
            </div>
            <span className={`text-sm font-bold ${layers.reports ? 'text-cyan-400' : 'text-slate-400'}`}>Verified Reports</span>
          </label>
        </div>
      </div>

      {/* Main Map */}
      <div className="flex-1 relative">
        <CityMap 
          hospitals={hospitals} 
          schools={schools} 
          roads={roads}
          zones={zones}
          reports={reports}
          showHospitals={layers.hospitals}
          showSchools={layers.schools}
          showRoads={layers.roads}
          showZones={layers.zones}
          showReports={layers.reports}
          onZoneClick={setSelectedZone}
        />
        
        {/* Timestamp */}
        {zones && zones.features.length > 0 && (
          <div className="absolute bottom-6 left-6 z-[400] bg-[#070b10]/90 backdrop-blur-md px-4 py-2 rounded-lg border border-white/10 text-xs text-slate-400">
            Last Updated: {new Date(zones.features[0].properties.generated_at).toLocaleString()}
          </div>
        )}
      </div>

      {/* Zone Intelligence Panel */}
      {selectedZone && (
        <div className="w-96 bg-[#070b10] border-l border-white/10 p-6 overflow-y-auto z-[401]">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-white">{selectedZone.name}</h2>
            <button onClick={() => setSelectedZone(null)} className="text-slate-400 hover:text-white">&times;</button>
          </div>
          
          <div className="space-y-6">
            <div className="bg-slate-800/50 rounded-xl p-4 border border-white/5">
              <div className="text-sm text-slate-400 uppercase tracking-wider mb-1">Overall Risk</div>
              <div className="flex items-end space-x-3">
                <span className="text-4xl font-bold text-white">{selectedZone.score_0_100}</span>
                <span className={`text-sm font-bold pb-1 ${
                  selectedZone.level === 'CRITICAL' ? 'text-rose-500' : 
                  selectedZone.level === 'HIGH' ? 'text-orange-500' : 
                  selectedZone.level === 'MODERATE' ? 'text-yellow-500' : 'text-emerald-500'
                }`}>{selectedZone.level}</span>
              </div>
              <div className="text-xs text-slate-500 mt-2">Confidence: {(selectedZone.confidence * 100).toFixed(1)}%</div>
            </div>

            <div>
              <h3 className="text-sm font-bold text-slate-300 mb-3">Dominant Risk</h3>
              <div className="px-3 py-2 bg-rose-500/10 text-rose-400 rounded border border-rose-500/20 font-bold inline-block">
                {selectedZone.risk_type}
              </div>
            </div>

            <WhyThisRiskPanel explanation={selectedZone.explainability} />
            
            <EmergencyResourcesPanel 
              zoneId={selectedZone.id} 
              riskType={selectedZone.risk_type} 
              riskScore={selectedZone.score_0_100}
            />

            <ResponseTwinPanel 
              zoneId={selectedZone.id} 
              currentScore={selectedZone.score_0_100} 
            />

            <div>
              <h3 className="text-sm font-bold text-slate-300 mb-3 mt-6">Recommended Actions</h3>
              <div className="bg-blue-500/10 text-blue-400 p-3 rounded-lg border border-blue-500/20 text-sm">
                <ul className="list-disc list-inside space-y-1">
                  <li>Deploy predictive flood barriers in {selectedZone.name}</li>
                  <li>Issue high-risk traffic advisory</li>
                </ul>
              </div>
            </div>
            
            <div className="pt-4 border-t border-white/10 text-xs text-slate-500">
              Data Freshness: <span className="text-slate-300">{selectedZone.data_freshness}</span><br/>
              Forecast Horizon: <span className="text-slate-300">{selectedZone.forecast_horizon}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
