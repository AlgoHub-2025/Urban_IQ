import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Bell, AlertTriangle, ShieldAlert, CheckCircle, Clock, Activity } from 'lucide-react';
import WhyThisRiskPanel from '../components/intelligence/WhyThisRiskPanel';
import EmergencyResourcesPanel from '../components/intelligence/EmergencyResourcesPanel';
import { useLanguage } from '../contexts/LanguageContext';

const API_BASE = 'http://localhost:8009/api';

export default function AlertCenter() {
  const { isUrdu } = useLanguage();
  const [alerts, setAlerts] = useState([]);
  const [filter, setFilter] = useState('active'); // active, acknowledged, resolved
  const [loading, setLoading] = useState(true);

  const fetchAlerts = async () => {
    try {
      const res = await axios.get(`${API_BASE}/alerts`);
      setAlerts(res.data.alerts);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStatusChange = async (alertId, action) => {
    try {
      await axios.post(`${API_BASE}/alerts/${alertId}/${action}`);
      fetchAlerts();
    } catch (e) {
      console.error(e);
    }
  };

  const filteredAlerts = alerts.filter(a => a.status === filter);
  const activeCount = alerts.filter(a => a.status === 'active').length;

  return (
    <div className="flex flex-col h-full animate-in fade-in duration-500 max-w-7xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between bg-[#0b0f14] border border-white/5 p-6 rounded-2xl">
        <div>
          <h1 className="text-2xl font-black text-white tracking-widest uppercase flex items-center">
            <Bell className="w-6 h-6 text-rose-500 mr-3" />
            Alert Center
          </h1>
          <p className="text-sm text-slate-400 mt-2">Centralized city risk alerts and emergency dispatch center.</p>
        </div>
        <div className="bg-rose-500/10 border border-rose-500/20 px-4 py-2 rounded-xl text-rose-400 font-bold flex items-center">
          <ShieldAlert className="w-5 h-5 mr-2" />
          {activeCount} ACTIVE
        </div>
      </div>

      {/* Tabs */}
      <div className="flex space-x-2 border-b border-white/5 pb-2">
        {['active', 'acknowledged', 'resolved'].map((tab) => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-6 py-3 rounded-t-xl font-bold text-sm tracking-widest uppercase transition-all ${
              filter === tab 
                ? 'bg-[#0b0f14] text-white border-t border-x border-white/10' 
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Alert Feed */}
      <div className="space-y-6">
        {loading && <div className="text-center text-slate-500 py-12">Loading alerts...</div>}
        {!loading && filteredAlerts.length === 0 && (
          <div className="flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-2xl py-24 text-slate-600">
            <CheckCircle className="w-12 h-12 mb-4 opacity-50" />
            <p className="font-bold tracking-widest uppercase">No {filter} alerts</p>
          </div>
        )}
        
        {filteredAlerts.map(alert => (
          <div key={alert.id} className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6 relative overflow-hidden">
            
            {/* Simulation Banner */}
            {alert.is_simulated && (
              <div className="absolute top-0 left-0 right-0 bg-rose-500/20 text-rose-400 text-[10px] font-black tracking-[0.2em] text-center py-1 uppercase">
                SIMULATED ALERT — Scenario Output (Not Live)
              </div>
            )}

            <div className={`mt-${alert.is_simulated ? '6' : '0'} flex flex-col md:flex-row justify-between items-start mb-6`}>
              <div>
                <div className="flex items-center space-x-3 mb-2">
                  <div className={`px-2 py-1 rounded text-[10px] font-black uppercase ${
                    alert.severity === 'CRITICAL' ? 'bg-rose-500 text-white' : 'bg-orange-500 text-white'
                  }`}>
                    {alert.severity}
                  </div>
                  <span className="text-sm font-bold text-slate-300">{alert.zone_id.replace('_', ' ').toUpperCase()}</span>
                </div>
                <h3 className="text-xl font-black text-white">{isUrdu && alert.title_ur ? alert.title_ur : alert.title}</h3>
                <p className="text-slate-400 mt-2 text-sm">{isUrdu && alert.message_ur ? alert.message_ur : alert.message}</p>
                <div className="flex items-center text-[10px] font-mono text-slate-500 mt-3">
                  <Clock className="w-3 h-3 mr-1" />
                  {new Date(alert.created_at).toLocaleString()}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col space-y-2 mt-4 md:mt-0 min-w-[150px]">
                {alert.status === 'active' && (
                  <button 
                    onClick={() => handleStatusChange(alert.id, 'acknowledge')} 
                    disabled={isViewer}
                    className={`px-4 py-2 text-white font-bold rounded-xl text-xs transition-colors ${isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'}`}
                  >
                    Acknowledge
                  </button>
                )}
                {['active', 'acknowledged'].includes(alert.status) && (
                  <button 
                    onClick={() => handleStatusChange(alert.id, 'resolve')} 
                    disabled={isViewer}
                    className={`px-4 py-2 text-white font-bold rounded-xl text-xs transition-colors ${isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-emerald-500 hover:bg-emerald-600'}`}
                  >
                    Resolve
                  </button>
                )}
                {alert.status === 'resolved' && (
                  <div className="px-4 py-2 bg-emerald-500/10 text-emerald-500 font-bold rounded-xl text-xs text-center border border-emerald-500/20">
                    RESOLVED
                  </div>
                )}
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-6 border-t border-white/5">
              
              <div>
                <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3">Recommended Actions</h4>
                <div className="bg-amber-500/5 border border-amber-500/10 rounded-xl p-4">
                  <ul className="space-y-2 text-xs text-amber-200/70">
                    {(isUrdu && alert.recommended_actions_ur && alert.recommended_actions_ur.length > 0 ? alert.recommended_actions_ur : alert.recommended_actions).map((act, i) => (
                      <li key={i} className="flex items-start">
                        <AlertTriangle className="w-4 h-4 text-amber-500 mr-2 flex-shrink-0" />
                        {act}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="mt-[-16px]">
                {alert.explainability && <WhyThisRiskPanel explanation={alert.explainability} />}
              </div>
            </div>

            <div className="mt-6 border-t border-white/5 pt-4">
              <details className="group">
                <summary className="flex items-center text-xs font-bold text-blue-400 cursor-pointer list-none">
                  <Activity className="w-4 h-4 mr-2" />
                  <span className="group-open:hidden">View Nearby Emergency Resources</span>
                  <span className="hidden group-open:inline">Hide Emergency Resources</span>
                </summary>
                <div className="mt-4">
                  <EmergencyResourcesPanel 
                    zoneId={alert.zone_id} 
                    riskType={alert.type} 
                    riskScore={alert.score}
                    isSimulated={alert.is_simulated}
                  />
                </div>
              </details>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}
