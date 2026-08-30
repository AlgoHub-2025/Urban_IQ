import React from 'react';
import { useAlerts } from '../hooks/useAlerts';
import { ShieldAlert, AlertTriangle, Info, Bell, Filter } from 'lucide-react';

export default function AlertsCenter() {
  const { alerts, loading } = useAlerts();

  const getIcon = (severity) => {
    switch(severity) {
      case 'critical': return <ShieldAlert className="w-5 h-5 text-rose-500" />;
      case 'warning': return <AlertTriangle className="w-5 h-5 text-amber-500" />;
      default: return <Info className="w-5 h-5 text-blue-500" />;
    }
  };

  const getStyle = (severity) => {
    switch(severity) {
      case 'critical': return "bg-rose-500/5 border-rose-500/20 text-rose-400";
      case 'warning': return "bg-amber-500/5 border-amber-500/20 text-amber-400";
      default: return "bg-blue-500/5 border-blue-500/20 text-blue-400";
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500 max-w-5xl mx-auto">
      
      <div className="flex justify-between items-end mb-8">
        <div>
          <h1 className="text-2xl font-black text-white flex items-center">
            <Bell className="w-6 h-6 mr-3 text-cyan-500" /> Operational Alerts Center
          </h1>
          <p className="text-slate-400 text-sm mt-2">Centralized feed of all systemic anomalies and ML predictions.</p>
        </div>
        <div className="flex space-x-2">
          <button className="flex items-center px-4 py-2 bg-[#0b0f14] border border-white/10 rounded-lg text-sm text-slate-300 hover:bg-white/5">
            <Filter className="w-4 h-4 mr-2" /> All Severities
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {loading ? (
          <div className="text-center p-12 text-slate-500 animate-pulse font-bold tracking-widest">SYNCING ALERTS...</div>
        ) : alerts.length === 0 ? (
          <div className="text-center p-12 text-emerald-500 font-bold bg-[#0b0f14] rounded-2xl border border-white/5">
            ALL SYSTEMS NORMAL
          </div>
        ) : (
          alerts.map((alert, i) => (
            <div key={i} className={`p-6 rounded-2xl border ${getStyle(alert.severity)} flex gap-6 items-start transition-all hover:bg-black/40`}>
              <div className="mt-1 bg-black/50 p-3 rounded-xl border border-white/5 shadow-xl">
                {getIcon(alert.severity)}
              </div>
              <div className="flex-1">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center space-x-3 mb-1">
                      <span className="text-[10px] font-bold uppercase tracking-widest bg-black/50 px-2 py-1 rounded">
                        {alert.category.replace('_', ' ')}
                      </span>
                      <span className="text-xs text-slate-500">Just now</span>
                    </div>
                    <h3 className="text-lg font-bold text-white mb-2">{alert.title}</h3>
                  </div>
                  <button className="text-xs font-bold px-4 py-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors text-white">
                    VIEW ON MAP
                  </button>
                </div>
                <p className="text-sm text-slate-300 leading-relaxed mb-4">{alert.message}</p>
                <div className="flex items-center space-x-4">
                  <span className="text-xs font-bold bg-black/30 px-3 py-1.5 rounded-lg text-slate-400">
                    📍 {alert.location}
                  </span>
                  {alert.value && (
                    <span className="text-xs font-bold bg-black/30 px-3 py-1.5 rounded-lg text-slate-400">
                      📊 Value: {alert.value}
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  );
}
