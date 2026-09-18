import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Camera, MapPin, Upload, CheckCircle, XCircle, AlertTriangle, ShieldCheck, Clock, FileText } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const API_BASE = 'http://localhost:8009/api';

const CATEGORIES = [
  "Waterlogging",
  "Road obstruction",
  "Smoke / air-quality issue",
  "Traffic issue",
  "Infrastructure issue",
  "Other"
];

export default function CitizenReports() {
  const { isViewer, isOperator } = useAuth();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitLoading, setSubmitLoading] = useState(false);
  
  // Form State
  const [file, setFile] = useState(null);
  const [category, setCategory] = useState(CATEGORIES[0]);
  const [description, setDescription] = useState("");
  const [zoneId, setZoneId] = useState("gulberg");
  const [lat, setLat] = useState("31.5204");
  const [lon, setLon] = useState("74.3587");

  useEffect(() => {
    fetchReports();
    // Simulate real-time mock location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setLat(pos.coords.latitude.toFixed(4));
          setLon(pos.coords.longitude.toFixed(4));
        },
        () => {}
      );
    }
  }, []);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/reports`);
      setReports(res.data.reports);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select an image");
    
    setSubmitLoading(true);
    const formData = new FormData();
    formData.append("image", file);
    formData.append("latitude", lat);
    formData.append("longitude", lon);
    formData.append("zone_id", zoneId);
    formData.append("category", category);
    formData.append("description", description);

    try {
      await axios.post(`${API_BASE}/reports`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setFile(null);
      setDescription("");
      fetchReports();
    } catch (e) {
      console.error(e);
      alert("Upload failed");
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleReview = async (id, action) => {
    try {
      await axios.post(`${API_BASE}/reports/${id}/${action}`, { notes: "Reviewed by operator" });
      fetchReports();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="flex flex-col h-full animate-in fade-in duration-500 max-w-7xl mx-auto space-y-6">
      
      <div className="flex items-center justify-between bg-[#0b0f14] border border-white/5 p-6 rounded-2xl">
        <div>
          <h1 className="text-2xl font-black text-white tracking-widest uppercase flex items-center">
            <Camera className="w-6 h-6 text-cyan-400 mr-3" />
            Citizen Intelligence
          </h1>
          <p className="text-sm text-slate-400 mt-2">
            Real-world observations supporting city intelligence. AI can detect signals, lekin final ground truth human verification ke baad banti hai.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Submission Form */}
        <div className="bg-[#0b0f14] border border-white/5 p-6 rounded-2xl">
          <h3 className="text-xs font-bold text-slate-500 tracking-widest uppercase mb-6 flex items-center">
            <FileText className="w-4 h-4 mr-2 text-cyan-500" />
            Submit Observation
          </h3>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-400 mb-2">Evidence Image</label>
              <div className="border-2 border-dashed border-slate-700 rounded-xl p-4 text-center hover:border-cyan-500/50 transition-colors">
                <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" id="fileUpload" />
                <label htmlFor="fileUpload" className="cursor-pointer flex flex-col items-center">
                  <Upload className="w-6 h-6 text-slate-500 mb-2" />
                  <span className="text-xs text-slate-400">{file ? file.name : "Click to upload image"}</span>
                </label>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-400 mb-2">Category</label>
              <select 
                value={category} 
                onChange={(e) => setCategory(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-sm text-white rounded-xl p-3 focus:outline-none focus:border-cyan-500"
              >
                {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-400 mb-2">Location (Lat)</label>
                <input type="text" value={lat} readOnly className="w-full bg-slate-900 border border-slate-700 text-sm text-slate-500 rounded-xl p-3" />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-400 mb-2">Location (Lon)</label>
                <input type="text" value={lon} readOnly className="w-full bg-slate-900 border border-slate-700 text-sm text-slate-500 rounded-xl p-3" />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-400 mb-2">Description</label>
              <textarea 
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 text-sm text-white rounded-xl p-3 h-24 focus:outline-none focus:border-cyan-500"
                placeholder="Describe the incident..."
                required
              />
            </div>

            <button 
              type="submit" 
              disabled={submitLoading}
              className="w-full py-3 bg-cyan-500 hover:bg-cyan-400 text-[#0b0f14] font-bold text-sm rounded-xl transition-colors disabled:opacity-50"
            >
              {submitLoading ? 'Uploading...' : 'Submit Report'}
            </button>
          </form>
        </div>

        {/* Dashboard */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-xs font-bold text-slate-500 tracking-widest uppercase px-2">Reports Dashboard</h3>
          
          {loading ? (
            <div className="text-center py-12 text-slate-500"><Clock className="w-6 h-6 mx-auto animate-spin mb-2" /> Loading reports...</div>
          ) : reports.length === 0 ? (
            <div className="text-center py-12 bg-[#0b0f14] border border-white/5 rounded-2xl">
              <ShieldCheck className="w-12 h-12 text-slate-700 mx-auto mb-4" />
              <p className="text-slate-500 font-bold uppercase tracking-widest text-sm">No reports submitted yet</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {reports.map(report => (
                <div key={report.id} className="bg-[#0b0f14] border border-white/5 rounded-2xl overflow-hidden flex flex-col">
                  <div className="h-40 bg-slate-900 relative">
                    <img src={report.image_url} alt="Incident" className="w-full h-full object-cover opacity-80" />
                    <div className="absolute top-2 right-2 flex space-x-2">
                      <span className={`px-2 py-1 text-[10px] font-bold rounded-lg uppercase ${
                        report.status === 'verified' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                        report.status === 'rejected' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
                        'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                      }`}>
                        {report.status}
                      </span>
                    </div>
                  </div>
                  <div className="p-4 flex-1 flex flex-col">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="text-white font-bold text-sm">{report.category}</h4>
                      <span className="text-[10px] text-slate-500 flex items-center"><MapPin className="w-3 h-3 mr-1" /> {report.zone_id}</span>
                    </div>
                    <p className="text-xs text-slate-400 mb-4 flex-1">{report.description}</p>
                    
                    {/* AI Assessment */}
                    <div className="bg-slate-900/50 p-3 rounded-lg border border-cyan-500/20 mb-4">
                      <p className="text-[10px] font-bold text-cyan-500 uppercase tracking-widest mb-1 flex items-center">
                        <AlertTriangle className="w-3 h-3 mr-1" /> AI Assessment
                      </p>
                      <p className="text-xs text-slate-300">{report.ai_classification}</p>
                      {report.ai_confidence && (
                        <p className="text-[10px] text-slate-500 mt-1">Confidence: {(report.ai_confidence * 100).toFixed(0)}%</p>
                      )}
                    </div>

                    {/* Operator Actions */}
                    {['pending', 'ai-assessed'].includes(report.status) && (
                      <div className="grid grid-cols-2 gap-2 mt-auto">
                        <button 
                          onClick={() => handleReview(report.id, 'verify')}
                          disabled={isViewer}
                          className={`flex items-center justify-center py-2 text-xs font-bold rounded-lg transition-colors ${isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 border border-emerald-500/30'}`}
                        >
                          <CheckCircle className="w-4 h-4 mr-1" /> Verify
                        </button>
                        <button 
                          onClick={() => handleReview(report.id, 'reject')}
                          disabled={isViewer}
                          className={`flex items-center justify-center py-2 text-xs font-bold rounded-lg transition-colors ${isViewer ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-rose-500/20 text-rose-400 hover:bg-rose-500/30 border border-rose-500/30'}`}
                        >
                          <XCircle className="w-4 h-4 mr-1" /> Reject
                        </button>
                      </div>
                    )}
                    {isViewer && ['pending', 'ai-assessed'].includes(report.status) && (
                      <p className="text-[9px] text-center text-rose-400 mt-2">Requires Operator Access</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
