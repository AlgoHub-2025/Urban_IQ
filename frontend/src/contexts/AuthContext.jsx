import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  // Hackathon demo roles: 'admin', 'operator', 'viewer'
  const [role, setRole] = useState('operator'); 

  useEffect(() => {
    const savedRole = localStorage.getItem('urbaniq_role');
    if (savedRole) setRole(savedRole);
  }, []);

  const changeRole = (newRole) => {
    setRole(newRole);
    localStorage.setItem('urbaniq_role', newRole);
  };

  // Inject role into axios interceptors
  useEffect(() => {
    const interceptorId = axios.interceptors.request.use(config => {
      config.headers['X-Role'] = role;
      return config;
    });

    return () => {
      axios.interceptors.request.eject(interceptorId);
    };
  }, [role]);

  return (
    <AuthContext.Provider value={{ role, changeRole, isAdmin: role === 'admin', isOperator: ['admin', 'operator'].includes(role), isViewer: role === 'viewer' }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
