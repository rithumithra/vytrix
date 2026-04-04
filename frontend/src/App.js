import React, { useState } from 'react';
import RegistrationPage from './components/RegistrationPage';
import PremiumPage from './components/PremiumPage';
import TriggerPage from './components/TriggerPage';
import ResultPage from './components/ResultPage';
import LoadingPage from './components/LoadingPage';

function App() {
  const [currentPage, setCurrentPage] = useState('registration');
  const [userData, setUserData] = useState(null);
  const [premiumData, setPremiumData] = useState(null);
  const [policyData, setPolicyData] = useState(null);
  const [resultData, setResultData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const showPage = (page) => {
    setCurrentPage(page);
    setError(null);
  };

  const showLoading = () => {
    setLoading(true);
    setError(null);
  };

  const hideLoading = () => {
    setLoading(false);
  };

  const showError = (message) => {
    setError(message);
    setLoading(false);
  };

  const handleRegistrationSuccess = (user, premium) => {
    setUserData(user);
    setPremiumData(premium);
    hideLoading();
    showPage('premium');
  };

  const handlePolicyActivation = (policy) => {
    setPolicyData(policy);
    hideLoading();
    showPage('trigger');
  };

  const handleSimulationResult = (result) => {
    setResultData(result);
    hideLoading();
    showPage('result');
  };

  if (loading) {
    return (
      <div className="container">
        <div className="header">
          <h1>🛡️ Vytrix</h1>
          <p>AI-Powered Income Protection for Gig Workers</p>
        </div>
        <LoadingPage />
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🛡️ Vytrix</h1>
        <p>AI-Powered Income Protection for Gig Workers</p>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {currentPage === 'registration' && (
        <RegistrationPage
          onSuccess={handleRegistrationSuccess}
          onLoading={showLoading}
          onError={showError}
        />
      )}

      {currentPage === 'premium' && (
        <PremiumPage
          userData={userData}
          premiumData={premiumData}
          onBack={() => showPage('registration')}
          onActivate={handlePolicyActivation}
          onLoading={showLoading}
          onError={showError}
        />
      )}

      {currentPage === 'trigger' && (
        <TriggerPage
          userData={userData}
          onBack={() => showPage('premium')}
          onSimulation={handleSimulationResult}
          onLoading={showLoading}
          onError={showError}
        />
      )}

      {currentPage === 'result' && (
        <ResultPage
          resultData={resultData}
          onBack={() => showPage('trigger')}
          onNewTest={() => showPage('trigger')}
        />
      )}
    </div>
  );
}

export default App;