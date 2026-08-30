import { AlertTriangle, ChevronRight } from 'lucide-react';

export default function AlertBanner({ alerts }) {
  if (!alerts || alerts.length === 0) return null;

  const critical = alerts.find(a => a.severity === 'critical') || alerts[0];

  return (
    <div className={`mb-6 p-4 rounded-xl border flex items-center justify-between ${
      critical.severity === 'critical' 
        ? 'bg-rose-500/10 border-rose-500/30' 
        : 'bg-amber-500/10 border-amber-500/30'
    }`}>
      <div className="flex items-center">
        <div className={`p-2 rounded-lg mr-4 ${
          critical.severity === 'critical' ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'
        }`}>
          <AlertTriangle className="w-5 h-5 animate-pulse" />
        </div>
        <div>
          <h4 className={`font-bold uppercase tracking-widest text-sm mb-0.5 ${
            critical.severity === 'critical' ? 'text-rose-400' : 'text-amber-400'
          }`}>
            {critical.severity} ALERT — {critical.category.replace('_', ' ')}
          </h4>
          <p className="text-slate-300 text-sm">{critical.message}</p>
        </div>
      </div>
      <button className={`text-sm font-bold flex items-center px-4 py-2 rounded-lg transition-colors ${
        critical.severity === 'critical' ? 'bg-rose-500/20 text-rose-400 hover:bg-rose-500/30' : 'bg-amber-500/20 text-amber-400 hover:bg-amber-500/30'
      }`}>
        View Alert <ChevronRight className="w-4 h-4 ml-1" />
      </button>
    </div>
  );
}
