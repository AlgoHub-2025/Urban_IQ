import React, { useState } from 'react';
import { useWeather } from '../hooks/useWeather';
import TemperatureChart from '../components/TemperatureChart';
import { CloudRain, Wind, ThermometerSun, Droplets } from 'lucide-react';

export default function WeatherDashboard() {
  const { weather, loading } = useWeather();
  const [activeMetric, setActiveMetric] = useState('temperature');

  if (loading) {
    return <div className="p-8 text-center text-slate-500 animate-pulse font-bold tracking-widest">LOADING ATMOSPHERIC DATA...</div>;
  }
  if (!weather || !weather.current) {
    return <div className="p-8 text-center text-rose-500">Failed to load weather data.</div>;
  }

  const { current } = weather;

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      
      {/* Hero Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-[#0b0f14] border border-amber-500/20 rounded-2xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10"><ThermometerSun className="w-24 h-24 text-amber-500" /></div>
          <p className="text-xs font-bold text-amber-500 tracking-widest uppercase mb-1">Temperature</p>
          <p className="text-5xl font-black text-white">{current.temperature_2m}°C</p>
          <p className="text-sm text-slate-400 mt-2">Feels like {current.apparent_temperature}°C</p>
        </div>
        
        <div className="bg-[#0b0f14] border border-blue-500/20 rounded-2xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10"><Droplets className="w-24 h-24 text-blue-500" /></div>
          <p className="text-xs font-bold text-blue-500 tracking-widest uppercase mb-1">Humidity</p>
          <p className="text-5xl font-black text-white">{current.relative_humidity_2m}%</p>
          <p className="text-sm text-slate-400 mt-2">Dew point critical evaluation</p>
        </div>

        <div className="bg-[#0b0f14] border border-cyan-500/20 rounded-2xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10"><Wind className="w-24 h-24 text-cyan-500" /></div>
          <p className="text-xs font-bold text-cyan-500 tracking-widest uppercase mb-1">Wind Speed</p>
          <p className="text-5xl font-black text-white">{current.wind_speed_10m} <span className="text-2xl">km/h</span></p>
          <p className="text-sm text-slate-400 mt-2">Surface level impact</p>
        </div>

        <div className="bg-[#0b0f14] border border-indigo-500/20 rounded-2xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10"><CloudRain className="w-24 h-24 text-indigo-500" /></div>
          <p className="text-xs font-bold text-indigo-500 tracking-widest uppercase mb-1">Precipitation</p>
          <p className="text-5xl font-black text-white">{current.precipitation} <span className="text-2xl">mm</span></p>
          <p className="text-sm text-slate-400 mt-2">Current accumulation</p>
        </div>
      </div>

      {/* Chart Section */}
      <div className="bg-[#0b0f14] border border-white/5 rounded-2xl p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-sm font-bold text-slate-300 tracking-widest uppercase">24-Hour Predictive Model</h2>
          <div className="flex space-x-2 bg-black/50 p-1 rounded-lg">
            <button className="px-4 py-1.5 rounded bg-amber-500/20 text-amber-400 text-xs font-bold">Temp</button>
            <button className="px-4 py-1.5 rounded hover:bg-white/5 text-slate-400 text-xs font-bold transition-colors">Rain</button>
            <button className="px-4 py-1.5 rounded hover:bg-white/5 text-slate-400 text-xs font-bold transition-colors">Wind</button>
          </div>
        </div>
        <TemperatureChart hourlyData={weather.hourly} />
      </div>
    </div>
  );
}
