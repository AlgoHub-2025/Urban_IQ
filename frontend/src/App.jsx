import { useState } from 'react';
import CommandCenterLayout from './layouts/CommandCenterLayout';

// Pages
import CityOverview from './pages/CityOverview';
import CityIntelligenceExplorer from './pages/CityIntelligenceExplorer';
import AlertsCenter from './pages/AlertsCenter';
import ReportForm from './components/ReportForm';

function App() {
  const [activeTab, setActiveTab] = useState('overview');

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'overview': return <CityOverview setActiveTab={setActiveTab} />;
      case 'intelligence': return <CityIntelligenceExplorer />;
      case 'alerts': return <AlertsCenter />;
      case 'report': return <ReportForm />;
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

export default App;
