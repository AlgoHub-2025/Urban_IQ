import React from 'react';
import { AlertTriangle, ChevronRight } from 'lucide-react';
import { useAlerts } from '../../hooks/useAlerts';

export default function GlobalAlertStrip() {
  const { alerts, loading } = useAlerts();

  if (loading || !alerts || alerts.length === 0) return null;

  // Find most severe alert
  const criticalAlert = alerts.find(a => a.severity === 'critical') || alerts[0];

  return (
    <div className="bg-rose-500/10 border-b border-rose-500/20 px-6 py-2.5 flex items-center justify-between group cursor-pointer hover:bg-rose-500/15 transition-colors">
      <div className="flex items-center max-w-[1600px] mx-auto w-full">
        <div className="flex items-center space-x-4 flex-1">
          <AlertTriangle className="w-4 h-4 text-rose-500 animate-pulse" />
          <span className="text-xs font-bold text-rose-400 tracking-widest uppercase flex-shrink-0">
            {criticalAlert.severity === 'critical' ? 'CRITICAL ALERT' : 'SYSTEM WARNING'}
          </span>
          <span className="text-rose-500/50">|</span>
          <span className="text-xs text-rose-200 font-medium truncate">
            <strong className="text-rose-100">{criticalAlert.title}:</strong> {criticalAlert.message}
          </span>
        </div>
        <button className="text-[10px] font-bold text-rose-400 flex items-center group-hover:text-rose-300 transition-colors tracking-widest flex-shrink-0">
          VIEW DETAILS <ChevronRight className="w-3.5 h-3.5 ml-1" />
        </button>
      </div>
    </div>
  );
}
