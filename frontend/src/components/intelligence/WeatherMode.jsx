import React, { useState } from 'react';
import { Sun, Cloud, CloudRain, CloudLightning, ChevronDown } from 'lucide-react';
import { useWeather } from '../../hooks/useWeather';
import TemperatureChart from '../TemperatureChart';

export default function WeatherMode() {
  const { weather, loading } = useWeather();
  const [selectedDayIndex, setSelectedDayIndex] = useState(0);

  if (loading) return <div className="text-xs text-slate-500 animate-pulse p-8">Loading atmospheric data...</div>;

  const forecast = weather?.forecast || [];
  if (forecast.length === 0) return null;

  const currentTemp = weather?.current?.temperature_2m || forecast[0].max_temp;
  
  const getWeatherDetails = (code) => {
    if (code === 0) return { desc: "Very warm with abundant sunshine", shortDesc: "Sunny", icon: Sun, iconColor: "text-amber-400" };
    if (code >= 1 && code <= 3) return { desc: "Partly cloudy with warm temperatures", shortDesc: "Cloudy", icon: Cloud, iconColor: "text-slate-300" };
    if (code >= 51 && code <= 67) return { desc: "Scattered showers", shortDesc: "Rain", icon: CloudRain, iconColor: "text-blue-400" };
    if (code >= 80 && code <= 82) return { desc: "Rain showers", shortDesc: "Showers", icon: CloudRain, iconColor: "text-blue-400" };
    if (code >= 95) return { desc: "Thunderstorms in the vicinity", shortDesc: "Storms", icon: CloudLightning, iconColor: "text-purple-400" };
    return { desc: "Very warm with abundant sunshine", shortDesc: "Sunny", icon: Sun, iconColor: "text-amber-400" };
  };

  const getDayName = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
  };

  const currentDetails = getWeatherDetails(forecast[0].weather_code);

  return (
    <div className="w-full max-w-4xl mx-auto bg-[#303134] rounded-3xl p-6 sm:p-8 text-[#e8eaed] shadow-2xl font-sans">
      
      {/* Header Info */}
      <div className="mb-8">
        <p className="text-[#9aa0a6] text-[15px] mb-4">Lahore, Pakistan</p>
        <div className="flex items-start">
          <span className="text-[64px] leading-none font-normal tracking-tighter">{currentTemp}°</span>
          <div className="ml-2 mt-2 flex text-lg text-[#9aa0a6]">
            <span className="text-white font-medium cursor-pointer">C</span>
            <span className="mx-2">|</span>
            <span className="cursor-pointer hover:text-white">F</span>
          </div>
        </div>
        <p className="text-[16px] text-[#e8eaed] mt-4 font-medium">{currentDetails.desc}</p>
      </div>

      {/* 8-Day Forecast Strip */}
      <div className="flex justify-between items-center overflow-x-auto gap-2 pb-4 scrollbar-hide mb-8">
        {forecast.slice(0, 8).map((day, idx) => {
          const details = getWeatherDetails(day.weather_code);
          const Icon = details.icon;
          const isSelected = selectedDayIndex === idx;

          return (
            <div 
              key={idx}
              onClick={() => setSelectedDayIndex(idx)}
              className={`flex flex-col items-center min-w-[70px] py-3 rounded-2xl cursor-pointer transition-colors ${
                isSelected ? 'bg-[#3c4043]' : 'hover:bg-white/5'
              }`}
            >
              <span className={`text-[15px] font-medium mb-3 ${isSelected ? 'text-white' : 'text-[#e8eaed]'}`}>
                {getDayName(day.date)}
              </span>
              <Icon className={`w-6 h-6 mb-3 ${details.iconColor}`} fill={details.iconColor === 'text-amber-400' ? 'currentColor' : 'none'} />
              <div className="flex flex-col items-center gap-1">
                <span className="text-[15px] font-bold text-white">{day.max_temp}°</span>
                <span className="text-[15px] font-medium text-[#9aa0a6]">{day.min_temp}°</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Dropdown Section */}
      <div className="flex items-center mb-6">
        <button className="flex items-center text-[15px] font-medium text-white hover:bg-white/5 px-2 py-1 rounded">
          Temperature <ChevronDown className="w-4 h-4 ml-1 opacity-70" />
        </button>
      </div>

      {/* Temperature Chart */}
      <div className="w-full mb-8">
         {/* Reusing existing chart component for hourly layout, though styled separately */}
         <TemperatureChart hourlyData={weather?.hourly || []} />
      </div>

      {/* Advanced Weather Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-8 pt-8 border-t border-white/10">
        
        {/* Humidity */}
        <div className="flex flex-col p-4 bg-[#3c4043]/30 rounded-2xl border border-white/5">
          <span className="text-[#9aa0a6] text-[13px] font-medium mb-1">Humidity</span>
          <span className="text-2xl font-medium text-[#e8eaed]">{weather?.current?.humidity}%</span>
        </div>

        {/* Wind Speed */}
        <div className="flex flex-col p-4 bg-[#3c4043]/30 rounded-2xl border border-white/5">
          <span className="text-[#9aa0a6] text-[13px] font-medium mb-1">Wind</span>
          <span className="text-2xl font-medium text-[#e8eaed]">{weather?.current?.wind_speed} <span className="text-[15px]">km/h</span></span>
        </div>

        {/* Feels Like */}
        <div className="flex flex-col p-4 bg-[#3c4043]/30 rounded-2xl border border-white/5">
          <span className="text-[#9aa0a6] text-[13px] font-medium mb-1">Feels Like</span>
          <span className="text-2xl font-medium text-[#e8eaed]">{weather?.current?.feels_like}°</span>
        </div>

        {/* UV Index */}
        <div className="flex flex-col p-4 bg-[#3c4043]/30 rounded-2xl border border-white/5">
          <span className="text-[#9aa0a6] text-[13px] font-medium mb-1">UV Index</span>
          <span className="text-2xl font-medium text-[#e8eaed]">{weather?.current?.uv_index} <span className="text-[15px] text-amber-400 font-bold ml-1">Very High</span></span>
        </div>

        {/* Visibility */}
        <div className="flex flex-col p-4 bg-[#3c4043]/30 rounded-2xl border border-white/5">
          <span className="text-[#9aa0a6] text-[13px] font-medium mb-1">Visibility</span>
          <span className="text-2xl font-medium text-[#e8eaed]">{weather?.current?.visibility} <span className="text-[15px]">km</span></span>
        </div>

        {/* Pressure */}
        <div className="flex flex-col p-4 bg-[#3c4043]/30 rounded-2xl border border-white/5">
          <span className="text-[#9aa0a6] text-[13px] font-medium mb-1">Pressure</span>
          <span className="text-2xl font-medium text-[#e8eaed]">{weather?.current?.pressure} <span className="text-[15px]">hPa</span></span>
        </div>

      </div>

    </div>
  );
}
