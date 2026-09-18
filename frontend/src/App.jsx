import { useState } from 'react';
import CommandCenterLayout from './layouts/CommandCenterLayout';

// Pages
import CityOverview from './pages/CityOverview';
import AlertsCenter from './pages/AlertsCenter';
import InteractiveMapPage from './pages/InteractiveMapPage';
import WhatIfSimulator from './pages/WhatIfSimulator';
import AIIncidentCommander from './pages/AIIncidentCommander';
import DataModelTrust from './pages/DataModelTrust';
import CitizenReports from './pages/CitizenReports';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'overview': return <CityOverview setActiveTab={setActiveTab} />;
      case 'intelligence': return <InteractiveMapPage />;
      case 'ai_commander': return <AIIncidentCommander />;
      case 'simulator': return <WhatIfSimulator />;
      case 'alerts': return <AlertsCenter />;
      case 'report': return <CitizenReports />;
      case 'trust': return <DataModelTrust />;
      default: return <CityOverview setActiveTab={setActiveTab} />;
    }
  };

  return (
    <CommandCenterLayout activeTab={activeTab} setActiveTab={setActiveTab}>
      <div className="animate-in fade-in duration-300">
        {renderActiveTab()}
      </div>
    </CommandCenterLayout>
  );
}
