import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Database, ShieldCheck, ShieldAlert, FileSearch, HelpCircle, Server, Activity, AlertTriangle, PlayCircle } from 'lucide-react';

const API_BASE = 'http://localhost:8009/api';

export default function DataModelTrust() {
  const [trustData, setTrustData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrust = async () => {
      try {
        const res = await axios.get(`${API_BASE}/trust/status`);
        setTrustData(res.data.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchTrust();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-slate-500 tracking-widest font-bold">LOADING TRUST LAYER...</div>;
  }

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'live': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'cached': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'fallback': return 'bg-amber-500/20 text-amber-400 border-amber-500/30';
      case 'unavailable': return 'bg-rose-500/20 text-rose-400 border-rose-500/30';
      case 'available': return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
      case 'loaded': return 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30';
      default: return 'bg-slate-800 text-slate-400 border-slate-700';
    }
  };

  const getFreshness = (seconds) => {
    if (seconds < 300) return <span className="text-emerald-400">Fresh (&lt; 5m)</span>;
    if (seconds < 1800) return <span className="text-amber-400">Aging (5-30m)</span>;
    return <span className="text-rose-400">Stale (&gt; 30m)</span>;
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-in fade-in duration-500 h-full overflow-y-auto pb-24">
      
      {/* Header */}
      <div className="bg-[#0b0f14] border border-white/5 p-8 rounded-2xl flex justify-between items-center relative overflow-hidden">
        <div className="relative z-10">
          <h1 className="text-2xl font-black text-white tracking-widest uppercase flex items-center mb-2">
            <ShieldCheck className="w-8 h-8 text-cyan-400 mr-3" />
            Data & Model Trust Center
          </h1>
          <p className="text-sm text-slate-400 max-w-2xl">
            Complete transparency into the data lineage, freshness, and model architecture powering Urban IQ.
          </p>
        </div>
        
        {trustData.system.demo_mode && (
          <div className="absolute top-0 right-0 p-8 h-full flex items-center bg-rose-500/5 border-l border-rose-500/20">
            <div className="text-right">
              <div className="flex items-center text-rose-400 font-black tracking-widest uppercase mb-1">
                <PlayCircle className="w-5 h-5 mr-2 animate-pulse" /> DEMO MODE ACTIVE
              </div>
              <p className="text-[10px] text-slate-500">Scenario simulation overrides are enabled.</p>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Live Data Sources */}
        <div>
          <h2 className="text-xs font-black text-slate-500 tracking-widest uppercase mb-4 flex items-center">
            <Database className="w-4 h-4 mr-2" /> Live Data Sources
          </h2>
          
          <div className="space-y-4">
            {trustData.data_sources.map((ds, idx) => (
              <div key={idx} className="bg-[#0b0f14] border border-white/5 rounded-xl p-5 relative overflow-hidden group hover:border-white/10 transition-colors">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-1">{ds.name}</h3>
                    <p className="text-xs text-blue-400 font-mono flex items-center">
                      <Server className="w-3 h-3 mr-1" /> {ds.provider}
                    </p>
                  </div>
                  <div className={`px-2 py-1 border rounded text-[10px] font-black uppercase tracking-widest ${getStatusColor(ds.status)}`}>
                    {ds.status}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4 text-xs bg-slate-900/50 rounded-lg p-3 mb-4">
                  <div>
                    <span className="block text-[10px] text-slate-500 uppercase font-bold mb-1">Freshness</span>
                    {getFreshness(ds.freshness_seconds)}
                  </div>
                  <div>
                    <span className="block text-[10px] text-slate-500 uppercase font-bold mb-1">Last Update</span>
                    <span className="text-slate-300">{new Date(ds.last_refresh).toLocaleTimeString()}</span>
                  </div>
                </div>

                {ds.limitations && ds.limitations.length > 0 && (
                  <div className="border-t border-white/5 pt-3">
                    <p className="text-[9px] text-slate-500 font-bold uppercase mb-2">Known Limitations</p>
                    <ul className="space-y-1">
                      {ds.limitations.map((lim, i) => (
                        <li key={i} className="text-[10px] text-slate-400 flex items-start">
                          <span className="text-amber-500 mr-1.5">•</span> {lim}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Model Registry */}
        <div>
          <h2 className="text-xs font-black text-slate-500 tracking-widest uppercase mb-4 flex items-center">
            <Activity className="w-4 h-4 mr-2" /> Model Registry
          </h2>
          
          <div className="space-y-4">
            {trustData.models.map((model, idx) => (
              <div key={idx} className="bg-[#0b0f14] border border-white/5 rounded-xl p-5">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-white mb-1">{model.name}</h3>
                    <p className="text-xs text-cyan-400 font-mono">{model.type}</p>
                  </div>
                  <div className="text-right">
                    <div className={`inline-block px-2 py-1 border rounded text-[10px] font-black uppercase tracking-widest mb-1 ${getStatusColor(model.status)}`}>
                      {model.status}
                    </div>
                    <div className="text-[10px] text-slate-500 font-mono">Ver: {model.version}</div>
                  </div>
                </div>

                <div className="bg-slate-900/50 rounded-lg p-3 mb-4">
                  <p className="text-[10px] text-slate-500 uppercase font-bold mb-2">Evaluation Metric</p>
                  {model.evaluation_metric.status === 'unavailable' ? (
                    <div className="text-xs text-rose-400/80 font-mono italic">
                      No certified evaluation metric natively available in registry.
                    </div>
                  ) : (
                    <div className="text-xs text-emerald-400 font-mono">
                      {model.evaluation_metric.name}: {model.evaluation_metric.value}
                    </div>
                  )}
                </div>

                {model.limitations && model.limitations.length > 0 && (
                  <div className="border-t border-white/5 pt-3">
                    <p className="text-[9px] text-slate-500 font-bold uppercase mb-2">Model Limitations</p>
                    <ul className="space-y-1">
                      {model.limitations.map((lim, i) => (
                        <li key={i} className="text-[10px] text-slate-400 flex items-start">
                          <span className="text-amber-500 mr-1.5">•</span> {lim}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* System Limitations Bottom Banner */}
      <div className="bg-rose-500/5 border border-rose-500/20 rounded-xl p-6 mt-8 flex items-start">
        <AlertTriangle className="w-5 h-5 text-rose-500 mr-4 flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="text-sm font-bold text-rose-400 mb-2 tracking-widest uppercase">System Operational Limitations</h3>
          <ul className="text-xs text-slate-400 space-y-1 list-disc list-inside">
            <li>Routing is not validated against live road closures. {trustData.system.routing_status === 'unavailable' && '(Currently disabled)'}</li>
            <li>Scenario results are fully simulated and isolated from production DB.</li>
            <li>Fallback data (when LIVE is unreachable) is strictly marked and never presented as live.</li>
            <li>Population estimates are ML predictions, not real-time sensory data.</li>
          </ul>
        </div>
      </div>

    </div>
  );
}
