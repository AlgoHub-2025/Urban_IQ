import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8009/api';

export function useWeather() {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_BASE}/weather`)
      .then(res => {
        setWeather(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Weather fetch failed", err);
        setLoading(false);
      });
  }, []);

  return { weather, loading };
}
