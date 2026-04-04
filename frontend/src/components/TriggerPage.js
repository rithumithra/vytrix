import React from 'react';
import axios from 'axios';

const TriggerPage = ({ userData, onBack, onSimulation, onLoading, onError }) => {
  const handleSimulation = async (scenarioType) => {
    onLoading();

    const endpoints = {
      'rain': '/api/simulate/rain',
      'fraud': '/api/simulate/fraud',
      'no-activity': '/api/simulate/no-activity'
    };

    try {
      const response = await axios.post(endpoints[scenarioType], {
        user_id: userData.user_id
      });

      const result = response.data;
      onSimulation(result);
    } catch (error) {
      console.error('Simulation error:', error);
      const errorMessage = error.response?.data?.detail || 'Simulation failed. Please try again.';
      onError(errorMessage);
    }
  };

  return (
    <div className="page">
      <button className="btn back-btn" onClick={onBack}>
        ← Back
      </button>
      
      <h2 style={{ marginBottom: '20px', color: '#333' }}>Test Scenarios</h2>
      
      <p style={{ marginBottom: '20px', color: '#666' }}>
        Click on any scenario to simulate claim processing:
      </p>

      <div className="simulation-buttons">
        <button 
          className="sim-btn rain" 
          onClick={() => handleSimulation('rain')}
        >
          <div className="sim-btn-title">🌧️ Simulate Rain</div>
          <div className="sim-btn-desc">Heavy rainfall affecting deliveries</div>
        </button>

        <button 
          className="sim-btn fraud" 
          onClick={() => handleSimulation('fraud')}
        >
          <div className="sim-btn-title">⚠️ Simulate Fraud</div>
          <div className="sim-btn-desc">Suspicious GPS and activity patterns</div>
        </button>

        <button 
          className="sim-btn no-activity" 
          onClick={() => handleSimulation('no-activity')}
        >
          <div className="sim-btn-title">📵 No Activity</div>
          <div className="sim-btn-desc">Complete cessation of delivery activity</div>
        </button>
      </div>

      {/* Information Card */}
      <div className="premium-card" style={{ marginTop: '30px' }}>
        <h4 style={{ marginBottom: '15px', color: '#333' }}>How It Works</h4>
        <div style={{ fontSize: '14px', color: '#666', lineHeight: '1.5' }}>
          <p style={{ marginBottom: '10px' }}>
            Our AI system analyzes multiple factors to determine claim eligibility:
          </p>
          <ul style={{ paddingLeft: '20px', marginBottom: '10px' }}>
            <li>Weather conditions (30% weight)</li>
            <li>Activity drop analysis (20% weight)</li>
            <li>Movement patterns (20% weight)</li>
            <li>Peer comparison (15% weight)</li>
            <li>Behavioral consistency (15% weight)</li>
          </ul>
          <p>
            Claims are automatically approved when the opportunity loss score exceeds 
            the dynamic threshold and fraud risk is low.
          </p>
        </div>
      </div>
    </div>
  );
};

export default TriggerPage;