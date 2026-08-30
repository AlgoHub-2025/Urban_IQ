import axios from 'axios';

const API_BASE = 'http://localhost:8009/api';

export const fetchIntelligence = async (query) => {
  const res = await axios.post(`${API_BASE}/analyze`, { query, location: "Lahore" });
  return res.data;
};

export const fetchWeather = async () => (await axios.get(`${API_BASE}/weather`)).data;
export const fetchAirQuality = async () => (await axios.get(`${API_BASE}/air-quality`)).data;
export const fetchHospitals = async () => (await axios.get(`${API_BASE}/hospitals`)).data;
export const fetchSchools = async () => (await axios.get(`${API_BASE}/schools`)).data;
export const fetchRoads = async () => (await axios.get(`${API_BASE}/roads`)).data;
export const fetchPopulation = async () => (await axios.get(`${API_BASE}/population`)).data;
export const fetchAlerts = async () => {
  const res = await axios.get(`${API_BASE}/alerts`);
  return res.data;
};

export const submitAqiReport = async (data) => {
  const res = await axios.post(`${API_BASE}/report-aqi`, data);
  return res.data;
};
