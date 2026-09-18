import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, Droplets, Wind, Car, ArrowRight, AlertTriangle, Users, Building, RefreshCw, Layers } from 'lucide-react';
import WhyThisRiskPanel from '../components/intelligence/WhyThisRiskPanel';
import { useAuth } from '../contexts/AuthContext';

const API_BASE = 'http://localhost:8009/api';

export default function WhatIfSimulator() {
  const { isViewer } = useAuth();
  const [params, setParams] = useState({
    rainfall_mm: 0,
    aqi: 0,
    traffic_mult: 1.0
  });
  
  const [results, setResults] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);

  const handleSimulate = async () => {
    setIsSimulating(true);
    try {
      const res = await axios.post(`${API_BASE}/simulator/run`, params);
      setResults(res.data.comparison);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSimulating(false);
    }
  };

  const handleReset = () => {
    setParams({ rainfall_mm: 0, aqi: 0, traffic_mult: 1.0 });
    setResults(null);
  };

  return (
    <div className="flex flex-col h-full animate-in fade-in duration-500 max-w-7xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="flex flex-col bg-[#0b0f14] border border-white/5 p-6 rounded-2xl">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-black text-white tracking-widest uppercase flex items-center">
              <Activity className="w-6 h-6 text-cyan-400 mr-3" />
              What-If Simulator
            </h1>
            <p className="text-sm text-slate-400 mt-2">Simulate hypothetical urban risk scenarios safely isolated from live production data.</p>
          </div>
          <div className="flex space-x-3">
            <button 
              onClick={handleReset}
              className="px-6 py-3 rounded-xl font-bold text-sm bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors"
            >
              Reset
            </button>
            <button 
              onClick={handleSimulate}
              disabled={isSimulating || isViewer}
              className={`px-6 py-3 rounded-xl font-bold text-sm transition-colors flex items-center ${isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-cyan-500 text-[#0b0f14] hover:bg-cyan-400 disabled:opacity-50'}`}
            >
              {isSimulating ? 'Simulating...' : isViewer ? 'Read Only (Viewers)' : 'Run Simulation'}
              {!isSimulating && !isViewer && <ArrowRight className="w-4 h-4 ml-2" />}
            </button>
          </div>
        </div>
        {isViewer && (
          <p className="text-right text-[10px] text-rose-400 mt-2">
            You need Operator access to run simulations.
          </p>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Controls Panel */}
        <div className="bg-[#0b0f14] border border-white/5 p-6 rounded-2xl space-y-8">
          <h3 className="text-xs font-bold text-slate-500 tracking-widest uppercase">Simulation Parameters</h3>
          
          {/* Rainfall */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-bold text-slate-300 flex items-center">
                <Droplets className="w-4 h-4 mr-2 text-blue-400" /> Rainfall Intensity
              </label>
              <span className="text-xs font-mono text-cyan-400">{params.rainfall_mm} mm</span>
            </div>
            <input 
              type="range" min="0" max="150" step="5"
              value={params.rainfall_mm}
              onChange={(e) => setParams({...params, rainfall_mm: Number(e.target.value)})}
              className="w-full accent-blue-500"
            />
          </div>

          {/* AQI */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-bold text-slate-300 flex items-center">
                <Wind className="w-4 h-4 mr-2 text-amber-400" /> Air Quality (AQI)
              </label>
              <span className="text-xs font-mono text-cyan-400">{params.aqi || 'Live Baseline'}</span>
            </div>
            <input 
              type="range" min="0" max="500" step="10"
              value={params.aqi}
              onChange={(e) => setParams({...params, aqi: Number(e.target.value)})}
              className="w-full accent-amber-500"
            />
          </div>

          {/* Traffic */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-sm font-bold text-slate-300 flex items-center">
                <Car className="w-4 h-4 mr-2 text-rose-400" /> Traffic Congestion
              </label>
              <span className="text-xs font-mono text-cyan-400">{params.traffic_mult.toFixed(1)}x Baseline</span>
            </div>
            <input 
              type="range" min="0.5" max="3.0" step="0.1"
              value={params.traffic_mult}
              onChange={(e) => setParams({...params, traffic_mult: Number(e.target.value)})}
              className="w-full accent-rose-500"
            />
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2 space-y-6">
          {!results ? (
            <div className="h-full min-h-[400px] flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-2xl">
              <Activity className="w-12 h-12 text-slate-700 mb-4" />
              <p className="text-slate-500 font-bold tracking-widest uppercase">Adjust parameters and run simulation</p>
            </div>
          ) : (
            <div className="space-y-4">
              <h3 className="text-xs font-bold text-slate-500 tracking-widest uppercase">Simulation Results</h3>
              {results.map((res, i) => (
                <div key={res.zone_id} className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6 relative overflow-hidden group hover:border-cyan-500/30 transition-colors">
                  
                  {/* Background indicator */}
                  {res.changes.score_change > 0 && <div className="absolute top-0 right-0 w-32 h-32 bg-rose-500/5 rounded-full blur-3xl" />}
                  
                  <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
                    <div>
                      <h4 className="text-lg font-black text-white uppercase tracking-wider flex items-center">
                        {res.zone_id.replace('_', ' ')}
                        <span className="ml-3 text-[9px] bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 px-2 py-0.5 rounded-full uppercase tracking-widest">{res.simulation_status}</span>
                      </h4>
                      <div className="flex flex-col space-y-1 mt-2 text-xs text-slate-400">
                        <span className="flex items-center"><Users className="w-3 h-3 mr-1" /> Exposed Pop: {res.baseline.exposed_population.toLocaleString()} → {res.simulated.exposed_population.toLocaleString()} (<span className="text-rose-400 ml-1">+{res.changes.population_change.toLocaleString()}</span>)</span>
                        <span className="flex items-center"><Activity className="w-3 h-3 mr-1" /> Exposed Facilities: {res.baseline.exposed_facilities} → {res.simulated.exposed_facilities} (<span className="text-rose-400 ml-1">+{res.changes.facility_change}</span>)</span>
                      </div>
                    </div>
                    
                    {/* Score comparison */}
                    <div className="flex items-center space-x-6 mt-4 md:mt-0">
                      <div className="text-center">
                        <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Baseline</p>
                        <p className="text-xl font-mono text-slate-300">{res.baseline.risk_score}</p>
                        <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full uppercase">{res.baseline.level}</span>
                      </div>
                      <ArrowRight className="w-5 h-5 text-slate-600" />
                      <div className="text-center">
                        <p className="text-[10px] text-cyan-500 font-bold uppercase tracking-widest">Simulated</p>
                        <p className="text-2xl font-mono text-white">{res.simulated.risk_score}</p>
                        <span className={`text-[10px] px-2 py-0.5 rounded-full uppercase font-bold ${res.simulated.level !== res.baseline.level ? 'bg-rose-500/20 text-rose-400 border border-rose-500/20' : 'bg-slate-800 text-slate-400'}`}>
                          {res.simulated.level}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Explainability Compare */}
                  <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 pt-4 border-t border-white/5">
                    <div>
                      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest text-center mb-2">Baseline Explanation</p>
                      <WhyThisRiskPanel explanation={res.changes.baseline_explanation} />
                    </div>
                    <div>
                      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest text-center mb-2">Simulated Explanation</p>
                      <WhyThisRiskPanel explanation={res.changes.simulated_explanation} />
                    </div>
                  </div>
                  
                  <div className="mt-6 pt-4 border-t border-white/5">
                    <h5 className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-3">Recommended Actions</h5>
                    <ul className="space-y-2 text-xs text-slate-400">
                      {res.changes.recommended_actions.map((act, idx) => (
                        <li key={idx} className="flex items-start">
                          <AlertTriangle className="w-3 h-3 text-amber-500 mr-2 mt-0.5 flex-shrink-0" />
                          {act}
                        </li>
                      ))}
                    </ul>
                  </div>

                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
