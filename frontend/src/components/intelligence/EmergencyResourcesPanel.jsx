import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Activity, MapPin, NavigationOff, ShieldCheck, ShieldAlert, Loader2 } from 'lucide-react';

const API_BASE = 'http://localhost:8009/api';

export default function EmergencyResourcesPanel({ zoneId, riskType, riskScore, isSimulated }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!zoneId) return;
    
    const fetchResources = async () => {
      setLoading(true);
      try {
        const res = await axios.get(`${API_BASE}/resources/${zoneId}`, {
          params: { risk_type: riskType, risk_score: riskScore, is_simulated: isSimulated ? 'true' : 'false' }
        });
        setData(res.data.data);
      } catch (e) {
        console.error("Failed to fetch emergency resources", e);
      } finally {
        setLoading(false);
      }
    };
    
    fetchResources();
  }, [zoneId, riskType, riskScore, isSimulated]);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-6 text-slate-500">
        <Loader2 className="w-5 h-5 animate-spin mr-2" />
        <span className="text-xs uppercase tracking-widest font-bold">Scanning Resources...</span>
      </div>
    );
  }

  if (!data || !data.resources || data.resources.length === 0) {
    return (
      <div className="bg-rose-500/10 border border-rose-500/20 p-4 rounded-xl mt-4">
        <p className="text-xs text-rose-400 font-bold flex items-center">
          <ShieldAlert className="w-4 h-4 mr-2" />
          No immediate emergency resources found within safe distance.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-[#0f151c] border border-white/5 rounded-2xl p-6 mt-4">
      <h3 className="text-xs font-black text-slate-500 tracking-widest uppercase mb-6 flex items-center">
        <Activity className="w-4 h-4 mr-2" />
        Nearby Emergency Resources
      </h3>

      <div className="space-y-4">
        {data.resources.map((resource, idx) => (
          <div key={idx} className="bg-[#151b23] border border-white/5 rounded-xl p-4">
            <div className="flex justify-between items-start mb-2">
              <h4 className="text-sm font-bold text-white flex items-center">
                <span className="w-5 h-5 rounded bg-blue-500/20 text-blue-400 flex items-center justify-center text-[10px] mr-2">H</span>
                {resource.name}
              </h4>
              <div className={`px-2 py-0.5 rounded text-[9px] font-black uppercase tracking-widest ${
                resource.priority_level === 'high' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                resource.priority_level === 'medium' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                'bg-slate-800 text-slate-400'
              }`}>
                Pri: {resource.priority_level}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2 mb-3 text-xs text-slate-400">
              <div className="flex items-center">
                <MapPin className="w-3 h-3 mr-1" />
                {resource.distance_km} km away
              </div>
              <div className="flex items-center">
                {resource.exposure_status === 'safe' ? (
                  <ShieldCheck className="w-3 h-3 text-emerald-500 mr-1" />
                ) : (
                  <ShieldAlert className="w-3 h-3 text-rose-500 mr-1" />
                )}
                Exp: {resource.exposure_status}
              </div>
            </div>

            <div className="pt-2 border-t border-white/5">
              <ul className="space-y-1">
                {resource.reason.map((r, i) => (
                  <li key={i} className="text-[10px] text-slate-500 flex items-start">
                    <span className="text-blue-500 mr-1.5">•</span> {r}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 p-3 bg-slate-800/50 rounded-lg border border-slate-700/50 flex items-start">
        <NavigationOff className="w-4 h-4 text-amber-500 mr-2 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-[10px] font-bold text-slate-300 uppercase tracking-widest mb-1">Routing: {data.routing_status}</p>
          <p className="text-[9px] text-slate-500">{data.limitations}</p>
        </div>
      </div>
    </div>
  );
}
