import React from "react";

export default function TemperatureChart({ hourlyData }) {
  if (!hourlyData || hourlyData.length === 0) return null;

  // Find min and max temp dynamically to scale properly
  const temps = hourlyData.map(item => item.temp);
  const minTemp = Math.min(...temps) - 2; 
  const maxTemp = Math.max(...temps) + 5;

  const width = Math.max(800, hourlyData.length * 80);
  const height = 140;

  const chartTop = 30;
  const chartBottom = height - 30;

  const xStep = width / Math.max(1, hourlyData.length - 1);

  const getY = (temp) => {
    const ratio = (temp - minTemp) / (maxTemp - minTemp);
    return chartBottom - ratio * (chartBottom - chartTop);
  };

  const points = hourlyData
    .map((item, index) => {
      const x = index * xStep;
      const y = getY(item.temp);
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div className="w-full">
      <div className="overflow-x-auto overflow-y-hidden scrollbar-hide pb-2">
        <div
          className="relative"
          style={{
            width: `${width}px`,
            height: `${height}px`,
          }}
        >
          {/* SVG Canvas */}
          <svg
            className="absolute inset-0 h-full w-full overflow-visible"
            viewBox={`0 0 ${width} ${height}`}
            preserveAspectRatio="none"
          >
            <defs>
              <linearGradient id="googleGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#a88053" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#a88053" stopOpacity="0" />
              </linearGradient>
            </defs>

            {/* Area under line */}
            <polygon
              points={`0,${height} ${points} ${width},${height}`}
              fill="url(#googleGradient)"
            />

            {/* Temperature line */}
            <polyline
              points={points}
              fill="none"
              stroke="#ffffff"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />

            {/* Temperature points */}
            {hourlyData.map((item, index) => {
              const x = index * xStep;
              const y = getY(item.temp);

              return (
                <circle
                  key={index}
                  cx={x}
                  cy={y}
                  r="4"
                  fill="#ffffff"
                />
              );
            })}
          </svg>

          {/* Temperature values (above dots) */}
          {hourlyData.map((item, index) => {
            const x = index * xStep;
            const y = getY(item.temp);

            return (
              <div
                key={index}
                className="absolute -translate-x-1/2 text-[15px] font-medium text-white"
                style={{
                  left: `${x}px`,
                  top: `${y - 28}px`,
                }}
              >
                {item.temp}&deg;
              </div>
            );
          })}

          {/* Time labels (bottom) */}
          {hourlyData.map((item, index) => {
            const x = index * xStep;

            // Format time. E.g., '6 PM' -> '6pm'
            const formattedTime = item.time.toLowerCase().replace(' ', '');

            return (
              <div
                key={index}
                className="absolute bottom-[-5px] -translate-x-1/2 whitespace-nowrap text-[13px] text-[#9aa0a6] font-medium"
                style={{
                  left: `${x}px`,
                }}
              >
                {formattedTime}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
