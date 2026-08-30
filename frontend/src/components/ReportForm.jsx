import React, { useState } from 'react';
import { Send, CheckCircle2, AlertTriangle } from 'lucide-react';
import { submitAqiReport } from '../services/api';

export default function ReportForm() {
  const [zone, setZone] = useState('');
  const [aqi, setAqi] = useState('');
  const [officerId, setOfficerId] = useState('');
  const [status, setStatus] = useState(null); // 'submitting', 'success', 'error'
  const [responseMsg, setResponseMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('submitting');
    
    try {
      const res = await submitAqiReport({
        zone,
        aqi: parseInt(aqi),
        officer_id: officerId
      });
      
      setStatus('success');
      setResponseMsg(res.message);
      
      // Reset form if it wasn't a critical alert
      if (!res.alert_triggered) {
        setZone('');
        setAqi('');
      }
    } catch (err) {
      setStatus('error');
      setResponseMsg('Failed to connect to the server. Please check your network.');
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500 max-w-3xl mx-auto">
      
      <div className="bg-slate-900/50 p-8 rounded-3xl border border-white/5 shadow-2xl">
        <div className="mb-8 border-b border-white/5 pb-6">
          <h2 className="text-2xl font-black text-white flex items-center">
            <AlertTriangle className="w-6 h-6 mr-3 text-amber-400" /> 
            Public Health & Safety Reporting
          </h2>
          <p className="text-slate-400 mt-2">
            Authorized health officials can securely log real-time environmental data. Critical readings will automatically dispatch emergency protocols and alert relevant authorities via email.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Authorized Officer ID</label>
              <input 
                type="text" 
                required
                value={officerId}
                onChange={(e) => setOfficerId(e.target.value)}
                className="w-full bg-[#0b0f14] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-500/50 transition-colors"
                placeholder="e.g. AUTH-4921"
              />
            </div>

            <div className="space-y-2">
              <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Lahore Zone / District</label>
              <select 
                required
                value={zone}
                onChange={(e) => setZone(e.target.value)}
                className="w-full bg-[#0b0f14] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-cyan-500/50 transition-colors appearance-none"
              >
                <option value="" disabled>Select Zone</option>
                <option value="Central Lahore">Central Lahore</option>
                <option value="Lahore Cantt">Lahore Cantt</option>
                <option value="Gulberg">Gulberg</option>
                <option value="Ravi">Ravi</option>
                <option value="Shalimar">Shalimar</option>
                <option value="Data Gunj Baksh">Data Gunj Baksh</option>
                <option value="Wagah">Wagah</option>
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest">Real-time AQI Reading (PM2.5)</label>
            <input 
              type="number" 
              required
              min="0"
              max="999"
              value={aqi}
              onChange={(e) => setAqi(e.target.value)}
              className="w-full bg-[#0b0f14] border border-white/10 rounded-xl px-4 py-4 text-3xl font-black text-white focus:outline-none focus:border-cyan-500/50 transition-colors text-center"
              placeholder="0"
            />
            <p className="text-xs text-slate-500 text-center mt-2">Values above 150 will instantly trigger emergency email dispatches.</p>
          </div>

          <button 
            type="submit" 
            disabled={status === 'submitting'}
            className="w-full py-4 rounded-xl font-bold tracking-wide transition-all bg-cyan-600 hover:bg-cyan-500 text-white flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {status === 'submitting' ? (
              <span className="animate-pulse">PROCESSING REPORT...</span>
            ) : (
              <>
                <Send className="w-5 h-5 mr-2" /> SUBMIT ENVIRONMENTAL INTELLIGENCE
              </>
            )}
          </button>
        </form>

        {status === 'success' && (
          <div className="mt-6 p-4 rounded-xl border border-emerald-500/30 bg-emerald-500/10 flex items-start animate-in zoom-in duration-300">
            <CheckCircle2 className="w-6 h-6 text-emerald-400 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-emerald-400 font-bold mb-1">Report Processed Successfully</h4>
              <p className="text-sm text-emerald-300/80">{responseMsg}</p>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
