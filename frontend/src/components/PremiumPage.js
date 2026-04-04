import React from 'react';
import axios from 'axios';

const PremiumPage = ({ userData, premiumData, onBack, onActivate, onLoading, onError }) => {
  const handleActivatePolicy = async () => {
    onLoading();

    try {
      const response = await axios.post('/api/policies/activate', {
        user_id: userData.user_id,
        coverage_type: premiumData.coverage_type,
        premium_amount: premiumData.final_premium
      });

      const policyData = response.data;
      onActivate(policyData);
    } catch (error) {
      console.error('Policy activation error:', error);
      const errorMessage = error.response?.data?.detail || 'Policy activation failed. Please try again.';
      onError(errorMessage);
    }
  };

  if (!premiumData) {
    return (
      <div className="page">
        <div className="error-message">
          Premium data not available. Please go back and register again.
        </div>
        <button className="btn back-btn" onClick={onBack}>
          ← Back
        </button>
      </div>
    );
  }

  return (
    <div className="page">
      <button className="btn back-btn" onClick={onBack}>
        ← Back
      </button>
      
      <h2 style={{ marginBottom: '20px', color: '#333' }}>Policy & Premium</h2>

      <div className="premium-card">
        <h3 style={{ marginBottom: '15px', color: '#4facfe' }}>
          Dynamic Premium Calculation
        </h3>
        
        <div className="premium-row">
          <span>Base Premium:</span>
          <span>₹{premiumData.base_premium}</span>
        </div>
        
        <div className="premium-row">
          <span>Zone Risk Adjustment:</span>
          <span>+₹{premiumData.zone_risk_adjustment}</span>
        </div>
        
        <div className="premium-row">
          <span>Weather Risk Adjustment:</span>
          <span>+₹{premiumData.weather_risk_adjustment}</span>
        </div>
        
        <div className="premium-row total">
          <span>Final Premium:</span>
          <span>₹{premiumData.final_premium}</span>
        </div>
        
        <div style={{ 
          marginTop: '15px', 
          paddingTop: '15px', 
          borderTop: '1px solid #ddd' 
        }}>
          <div className="premium-row">
            <span>Coverage Amount:</span>
            <span>₹{premiumData.coverage_amount.toLocaleString()}</span>
          </div>
          <div className="premium-row">
            <span>Coverage Type:</span>
            <span style={{ textTransform: 'capitalize' }}>
              {premiumData.coverage_type.replace('_', ' ')}
            </span>
          </div>
        </div>
      </div>

      {/* Risk Factors Display */}
      <div className="premium-card">
        <h4 style={{ marginBottom: '15px', color: '#333' }}>Risk Assessment</h4>
        <div className="premium-row">
          <span>Zone Risk Factor:</span>
          <span>{(premiumData.risk_factors.zone_risk * 100).toFixed(1)}%</span>
        </div>
        <div className="premium-row">
          <span>Weather Risk Factor:</span>
          <span>{(premiumData.risk_factors.weather_risk * 100).toFixed(1)}%</span>
        </div>
        <div className="premium-row">
          <span>User Risk Score:</span>
          <span>{(premiumData.risk_factors.user_risk * 100).toFixed(1)}%</span>
        </div>
        <div className="premium-row">
          <span>Vehicle Risk Factor:</span>
          <span>{(premiumData.risk_factors.vehicle_risk * 100).toFixed(1)}%</span>
        </div>
      </div>

      <button className="btn" onClick={handleActivatePolicy}>
        Activate Plan
      </button>
    </div>
  );
};

export default PremiumPage;