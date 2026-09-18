import React, { createContext, useState, useContext, useEffect } from 'react';

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('en'); // 'en' or 'ur'

  // Load from local storage if available
  useEffect(() => {
    const saved = localStorage.getItem('urbaniq_lang');
    if (saved) setLanguage(saved);
  }, []);

  const toggleLanguage = () => {
    const nextLang = language === 'en' ? 'ur' : 'en';
    setLanguage(nextLang);
    localStorage.setItem('urbaniq_lang', nextLang);
  };

  return (
    <LanguageContext.Provider value={{ language, toggleLanguage, isUrdu: language === 'ur' }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLanguage = () => useContext(LanguageContext);
