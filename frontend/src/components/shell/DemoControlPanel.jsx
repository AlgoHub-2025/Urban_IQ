import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { AlertTriangle, Play, RotateCcw } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const API_BASE = 'http://localhost:8009/api';

export default function DemoControlPanel() {
  const [demoState, setDemoState] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);
  const { isViewer } = useAuth();

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE}/demo/status`);
      setDemoState(res.data);
    } catch (error) {
      console.error("Failed to fetch demo status");
    }
  };

  useEffect(() => {
    fetchStatus();
    // Poll every 5s just in case
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleRunDemo = async () => {
    setIsUpdating(true);
    try {
      await axios.post(`${API_BASE}/demo/scenario/heavy-rain`);
      await fetchStatus();
      // Force reload page to refresh map zones + AI state for demo effect
      window.location.reload(); 
    } catch (error) {
      console.error(error);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleResetDemo = async () => {
    setIsUpdating(true);
    try {
      await axios.post(`${API_BASE}/demo/reset`);
      await fetchStatus();
      window.location.reload();
    } catch (error) {
      console.error(error);
    } finally {
      setIsUpdating(false);
    }
  };

  if (!demoState) return null;

  return (
    <div className="fixed bottom-6 left-6 z-[9999] flex flex-col gap-2 animate-in slide-in-from-bottom-5">
      {demoState.is_active && (
        <div className="bg-rose-500/90 backdrop-blur-md border border-rose-500 text-white px-4 py-2 rounded-xl shadow-[0_0_20px_rgba(244,63,94,0.3)] flex items-center mb-2">
          <AlertTriangle className="w-5 h-5 mr-3 animate-pulse" />
          <div>
            <h4 className="text-xs font-black tracking-widest uppercase">DEMO MODE ACTIVE</h4>
            <p className="text-[10px] opacity-80">Deterministic hackathon scenario — not live data</p>
          </div>
        </div>
      )}

      <div className="bg-[#0b0f14]/90 backdrop-blur-xl border border-white/10 p-2 rounded-2xl flex flex-col gap-2 shadow-2xl">
        <div className="px-2 pt-1">
          <p className="text-[9px] font-bold text-slate-500 tracking-widest uppercase">Demo Controls</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleRunDemo}
            disabled={isUpdating || isViewer}
            className={`flex items-center px-4 py-2 rounded-xl text-xs font-bold transition-all ${isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-indigo-500/20 hover:bg-indigo-500/40 text-indigo-400 border border-indigo-500/30'}`}
          >
            <Play className="w-4 h-4 mr-2" />
            Run Heavy Rain
          </button>
          
          <button
            onClick={handleResetDemo}
            disabled={isUpdating || isViewer}
            className={`flex items-center px-4 py-2 rounded-xl text-xs font-bold transition-all ${isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5'}`}
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset Live Data
          </button>
        </div>
      </div>
    </div>
  );
}
