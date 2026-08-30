import { MapContainer, TileLayer, CircleMarker, Popup, Polyline, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Standard OpenStreetMap (We will apply a CSS filter to make it a perfect dark mode)
const DARK_MAP_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

export default function CityMap({ hospitals, schools, roads, showHospitals, showSchools, showRoads, showPop }) {
  // Center of Lahore
  const position = [31.5204, 74.3587];

  const getRiskColor = (confidence) => {
    if (confidence > 0.9) return '#10b981'; // Green
    if (confidence > 0.7) return '#eab308'; // Yellow
    return '#ef4444'; // Red
  };

  return (
    <div className="absolute inset-0 rounded-2xl overflow-hidden border border-white/10 shadow-2xl z-0">
      <style>
        {`
          .leaflet-tile-pane {
            filter: invert(100%) hue-rotate(180deg) brightness(100%) contrast(100%);
          }
        `}
      </style>
      <MapContainer center={position} zoom={12} className="h-full w-full bg-[#0a0f18]">
        <TileLayer
          url={DARK_MAP_URL}
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {showHospitals && (hospitals?.predictions || []).map((h, i) => {
          if (!h.lat || !h.lon) return null;
          return (
          <CircleMarker
            key={`h-${i}`}
            center={[h.lat, h.lon]}
            radius={8}
            pathOptions={{ color: getRiskColor(h.confidence), fillColor: getRiskColor(h.confidence), fillOpacity: 0.8, weight: 2 }}
          >
            <Tooltip direction="top" offset={[0, -10]} opacity={0.9}>
              <span className="font-bold">{h.name !== 'Unknown' ? h.name : 'Clinic'}</span>
            </Tooltip>
            <Popup className="bg-slate-900 border-none">
              <div className="p-2">
                <h4 className="font-bold text-slate-800">{h.name !== 'Unknown' ? h.name : 'Unregistered Clinic'}</h4>
                <p className="text-sm">Type: {h.predicted_type}</p>
                <p className="text-sm">Confidence: {(h.confidence * 100).toFixed(1)}%</p>
                <button className="mt-2 text-xs text-blue-600 font-bold">View Intelligence</button>
              </div>
            </Popup>
          </CircleMarker>
        )})}

        {showSchools && (schools?.predictions || []).map((s, i) => {
          if (!s.lat || !s.lon) return null;
          return (
          <CircleMarker
            key={`s-${i}`}
            center={[s.lat, s.lon]}
            radius={6}
            pathOptions={{ color: '#818cf8', fillColor: '#6366f1', fillOpacity: 0.8, weight: 2 }}
          >
            <Tooltip direction="top" offset={[0, -10]} opacity={0.9}>
              <span className="font-bold">{s.name !== 'Unknown' ? s.name : 'School'}</span>
            </Tooltip>
            <Popup>
              <h4 className="font-bold">{s.name !== 'Unknown' ? s.name : 'Unknown School'}</h4>
              <p>Type: {s.predicted_type}</p>
            </Popup>
          </CircleMarker>
        )})}

        {showRoads && (roads?.predictions || []).slice(0, 500).map((r, i) => {
          if (!r.lat || !r.lon) return null;
          return (
          <CircleMarker
            key={`r-${i}`}
            center={[r.lat, r.lon]}
            radius={2}
            pathOptions={{ color: '#94a3b8', stroke: false, fillOpacity: 0.8 }}
          />
        )})}

      </MapContainer>
    </div>
  );
}
