import React from 'react';
import { Info, CheckCircle, Database, ShieldAlert, Cpu } from 'lucide-react';

export default function WhyThisRiskPanel({ explanation }) {
  if (!explanation) return null;

  return (
    <div className="bg-[#0f151c] border border-white/5 rounded-2xl p-6 mt-4">
      <h3 className="text-xs font-black text-slate-500 tracking-widest uppercase mb-6 flex items-center">
        <Info className="w-4 h-4 mr-2" />
        Why This Risk?
      </h3>

      {/* Header Info */}
      <div className="flex items-center justify-between mb-6 pb-6 border-b border-white/5">
        <div>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Risk Score</p>
          <div className="flex items-center mt-1">
            <span className="text-2xl font-mono text-white mr-2">{explanation.score}</span>
            <span className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded-full uppercase">{explanation.risk_type}</span>
          </div>
        </div>
        <div className="text-right">
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Updated</p>
          <p className="text-xs text-slate-300 mt-1 font-mono">
            {new Date(explanation.generated_at).toLocaleTimeString('en-PK', { timeZone: 'Asia/Karachi' })} PKT
          </p>
        </div>
      </div>

      {/* Top Contributors */}
      <div className="mb-6">
        <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-4">Top Contributors</p>
        <div className="space-y-4">
          {explanation.top_factors.map((factor, idx) => (
            <div key={idx}>
              <div className="flex justify-between items-center text-xs mb-1">
                <span className="text-slate-300 flex items-center">
                  {factor.direction === 'increases_risk' ? <span className="text-rose-400 mr-1">↑</span> : <span className="text-emerald-400 mr-1">↓</span>}
                  {factor.factor}
                </span>
                <span className="font-mono text-slate-400">{factor.normalized_contribution}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div 
                  className={`h-full rounded-full ${factor.direction === 'increases_risk' ? 'bg-rose-500' : 'bg-emerald-500'}`}
                  style={{ width: `${Math.min(factor.normalized_contribution, 100)}%` }}
                />
              </div>
              <div className="flex justify-between items-center mt-1 text-[9px] text-slate-600 uppercase">
                <span className="flex items-center">
                  <Database className="w-2.5 h-2.5 mr-1" />
                  {factor.source}
                </span>
                <span className="flex items-center">
                  <Cpu className="w-2.5 h-2.5 mr-1" />
                  {factor.quality}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Evidence & Confidence */}
      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/5">
        <div>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-2">Evidence Grounding</p>
          <ul className="space-y-1">
            {explanation.evidence.map((ev, i) => (
              <li key={i} className="text-[10px] text-slate-400 flex items-start leading-tight">
                <CheckCircle className="w-3 h-3 text-emerald-500 mr-1 flex-shrink-0 mt-0.5" />
                {ev}
              </li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mb-2">Model Confidence</p>
          <div className="flex items-center">
            <ShieldAlert className="w-4 h-4 text-cyan-400 mr-2" />
            <span className="text-xl font-mono text-white">{(explanation.confidence * 100).toFixed(0)}%</span>
          </div>
          <p className="text-[9px] text-slate-500 mt-1 uppercase">Method: {explanation.explanation_type}</p>
        </div>
      </div>
    </div>
  );
}
