import { MapContainer, TileLayer, CircleMarker, Popup, Tooltip, GeoJSON } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const DARK_MAP_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";

export default function CityMap({ 
  hospitals, 
  schools, 
  roads, 
  zones, 
  reports = [],
  showHospitals = true,
  showSchools = true,
  showRoads = true,
  showZones = true,
  showReports = true,
  onZoneClick 
}) {
  const position = [31.5204, 74.3587];

  const getRiskColor = (confidence) => {
    if (confidence > 0.9) return '#10b981'; 
    if (confidence > 0.7) return '#eab308'; 
    return '#ef4444'; 
  };

  const getZoneColor = (level) => {
    if (level === 'CRITICAL') return '#f43f5e'; // rose-500
    if (level === 'HIGH') return '#f97316'; // orange-500
    if (level === 'MODERATE') return '#eab308'; // yellow-500
    return '#10b981'; // emerald-500
  };

  const onEachFeature = (feature, layer) => {
    layer.on({
      click: () => {
        if (onZoneClick) onZoneClick(feature.properties);
      },
      mouseover: (e) => {
        const layer = e.target;
        layer.setStyle({ weight: 3, fillOpacity: 0.5 });
      },
      mouseout: (e) => {
        const layer = e.target;
        layer.setStyle({ weight: 1, fillOpacity: 0.2 });
      }
    });
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
      <MapContainer center={position} zoom={11} className="h-full w-full bg-[#0a0f18]">
        <TileLayer
          url={DARK_MAP_URL}
          attribution='&copy; OpenStreetMap'
        />

        {showZones && zones && (
          <GeoJSON 
            key={JSON.stringify(zones)} // Force re-render on data change
            data={zones}
            style={(feature) => ({
              color: getZoneColor(feature.properties.level),
              weight: 1,
              fillColor: getZoneColor(feature.properties.level),
              fillOpacity: 0.2
            })}
            onEachFeature={onEachFeature}
          />
        )}

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

        {showReports && reports.map((r, i) => {
          if (!r.latitude || !r.longitude) return null;
          return (
            <CircleMarker
              key={`rep-${i}`}
              center={[r.latitude, r.longitude]}
              radius={8}
              pathOptions={{ color: '#06b6d4', fillColor: '#06b6d4', stroke: true, weight: 2, fillOpacity: 0.9 }}
            >
              <Popup className="bg-[#0b0f14] border border-white/10 text-white rounded-xl">
                <div className="p-1">
                  <span className="text-[10px] uppercase font-bold tracking-widest text-emerald-400 block mb-1">✓ Verified Report</span>
                  <span className="font-bold text-sm block mb-1">{r.category}</span>
                  <span className="text-xs text-slate-300 block">{r.description}</span>
                  {r.image_url && <img src={r.image_url} alt="Report" className="w-full h-24 object-cover mt-2 rounded-lg opacity-80" />}
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
}
