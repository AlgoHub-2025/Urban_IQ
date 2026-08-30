import React from 'react';
import Header from '../components/shell/Header';
import GlobalAlertStrip from '../components/shell/GlobalAlertStrip';

export default function CommandCenterLayout({ children, activeTab, setActiveTab }) {
  return (
    <div className="min-h-screen bg-[#070b10] text-slate-300 font-sans selection:bg-cyan-500/30">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      <GlobalAlertStrip />
      <main className="max-w-[1600px] mx-auto p-6">
        {children}
      </main>
    </div>
  );
}
