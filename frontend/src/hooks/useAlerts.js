import { useState, useEffect } from 'react';
import { fetchAlerts } from '../services/api';

export function useAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts().then(data => {
      setAlerts(data.alerts || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  return { alerts, loading };
}
