import React, { useState } from 'react';
import axios from 'axios';
import { Network, ArrowRight, Activity, Cpu, ShieldAlert } from 'lucide-react';
import { useLanguage } from '../../contexts/LanguageContext';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE = 'http://localhost:8009/api';

const ACTIONS = [
  { id: 'traffic_diversion', label: 'Traffic Diversion', icon: Network },
  { id: 'drainage_clearance', label: 'Drainage Clearance', icon: Activity },
  { id: 'resource_pre_deployment', label: 'Pre-Deploy Resources', icon: ShieldAlert }
];

export default function ResponseTwinPanel({ zoneId, currentScore }) {
  const { isUrdu } = useLanguage();
  const { isViewer } = useAuth();
  const [selectedAction, setSelectedAction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const simulateAction = async (actionId) => {
    setSelectedAction(actionId);
    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post(`${API_BASE}/twin/evaluate-action`, {
        zone_id: zoneId,
        action: actionId
      });
      setResult(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#0b0f14] border border-white/10 rounded-2xl p-6 mt-6 overflow-hidden relative">
      {/* Background glow */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 blur-3xl rounded-full" />
      
      <div className="relative z-10">
        <h3 className="text-sm font-black text-cyan-400 tracking-widest uppercase mb-4 flex items-center">
          <Cpu className="w-4 h-4 mr-2" /> Urban Response Twin
        </h3>
        
        <p className="text-xs text-slate-400 mb-6 max-w-md">
          Prediction tells us what may happen. Response Twin helps us test what we can do about it. Select an intervention to simulate its impact.
        </p>

        {/* Action Selector */}
        <div className="flex flex-wrap gap-2 mb-6">
          {ACTIONS.map(action => (
            <button
              key={action.id}
              onClick={() => simulateAction(action.id)}
              disabled={loading || isViewer}
              className={`flex items-center px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                selectedAction === action.id 
                  ? 'bg-cyan-500 text-white shadow-[0_0_15px_rgba(6,182,212,0.3)]' 
                  : isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-white/5 text-slate-400 hover:bg-white/10 hover:text-slate-200'
              } ${loading && selectedAction !== action.id ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              <action.icon className="w-4 h-4 mr-2" />
              {action.label}
            </button>
          ))}
        </div>
        {isViewer && (
          <p className="text-[10px] text-rose-400 mt-2 mb-4">
            You need Operator access to run twin simulations.
          </p>
        )}

        {/* Simulation Results */}
        {loading && (
          <div className="py-8 text-center text-cyan-400 animate-pulse text-xs tracking-widest font-bold uppercase">
            Simulating Impact Matrix...
          </div>
        )}

        {result && !loading && (
          <div className="bg-slate-900/80 border border-cyan-500/30 rounded-xl p-5 animate-in fade-in slide-in-from-bottom-2 duration-300">
            
            <div className="flex justify-between items-center mb-6">
              <div className="text-center">
                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Current Risk</p>
                <div className="text-3xl font-black text-rose-500">{result.baseline_risk}</div>
              </div>
              
              <div className="flex flex-col items-center px-4">
                <ArrowRight className="w-6 h-6 text-slate-600 mb-1" />
                <div className="bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full text-[10px] font-black tracking-widest border border-emerald-500/20">
                  {result.expected_impact}
                </div>
              </div>

              <div className="text-center">
                <p className="text-[10px] font-bold text-cyan-500 uppercase tracking-widest mb-1">Simulated Risk</p>
                <div className="text-3xl font-black text-cyan-400">{result.after_action_risk}</div>
              </div>
            </div>

            <div className="pt-4 border-t border-white/5 space-y-3">
              <div>
                <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">Affected Factors</p>
                <div className="flex gap-2">
                  {result.affected_factors.map(f => (
                    <span key={f} className="bg-white/5 px-2 py-1 rounded text-[10px] text-slate-300">{f}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">AI Explanation</p>
                <p className="text-xs text-slate-300 leading-relaxed border-l-2 border-cyan-500/50 pl-3 italic">
                  "{isUrdu && result.explanation_ur ? result.explanation_ur : result.explanation}"
                </p>
              </div>
            </div>

          </div>
        )}
      </div>
    </div>
  );
}
