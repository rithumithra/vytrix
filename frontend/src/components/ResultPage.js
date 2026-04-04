import React from 'react';

const ResultPage = ({ resultData, onBack, onNewTest }) => {
  if (!resultData) {
    return (
      <div className="page">
        <div className="error-message">
          Result data not available. Please go back and run a simulation.
        </div>
        <button className="btn back-btn" onClick={onBack}>
          ← Back to Scenarios
        </button>
      </div>
    );
  }

  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case 'approved':
        return 'approved';
      case 'rejected':
        return 'rejected';
      case 'under_review':
        return 'under-review';
      default:
        return 'approved';
    }
  };

  const formatScore = (score) => {
    return typeof score === 'number' ? score.toFixed(2) : '0.00';
  };

  return (
    <div className="page">
      <button className="btn back-btn" onClick={onBack}>
        ← Back to Scenarios
      </button>
      
      <h2 style={{ marginBottom: '20px', color: '#333' }}>Claim Result</h2>

      <div className="result-card">
        <div className="result-header">
          <h3>Claim Processing Complete</h3>
          <span className={`status ${getStatusClass(resultData.status)}`}>
            {resultData.status}
          </span>
        </div>

        <div className="score-display">
          <div className="score-item">
            <div className="score-value">
              {formatScore(resultData.opportunity_score)}
            </div>
            <div className="score-label">Opportunity Score</div>
          </div>
          <div className="score-item">
            <div className="score-value">
              {formatScore(resultData.fraud_score)}
            </div>
            <div className="score-label">Fraud Score</div>
          </div>
        </div>

        <div style={{ textAlign: 'center', margin: '15px 0' }}>
          <div style={{ fontSize: '14px', color: '#666' }}>
            Threshold: {formatScore(resultData.threshold)}
          </div>
          {resultData.claim_amount && (
            <div style={{ 
              fontSize: '18px', 
              fontWeight: 'bold', 
              color: '#4facfe', 
              marginTop: '10px' 
            }}>
              Payout: ₹{resultData.claim_amount}
            </div>
          )}
        </div>

        <div className="reasons">
          <h4>Decision Factors:</h4>
          <ul>
            {resultData.reasons && resultData.reasons.length > 0 ? (
              resultData.reasons.map((reason, index) => (
                <li key={index}>{reason}</li>
              ))
            ) : (
              <li>Standard processing completed</li>
            )}
          </ul>
        </div>

        {/* Score Breakdown */}
        {resultData.score_breakdown && (
          <div style={{ marginTop: '20px' }}>
            <h4 style={{ marginBottom: '15px', color: '#333' }}>Score Breakdown</h4>
            <div style={{ fontSize: '14px' }}>
              {Object.entries(resultData.score_breakdown).map(([key, value]) => {
                if (typeof value === 'object' && value.score !== undefined) {
                  return (
                    <div key={key} className="premium-row" style={{ fontSize: '12px' }}>
                      <span style={{ textTransform: 'capitalize' }}>
                        {key.replace('_', ' ')}:
                      </span>
                      <span>
                        {formatScore(value.score)} × {value.weight} = {formatScore(value.contribution)}
                      </span>
                    </div>
                  );
                }
                return null;
              })}
            </div>
          </div>
        )}

        {/* Processing Information */}
        <div style={{ 
          marginTop: '20px', 
          paddingTop: '15px', 
          borderTop: '1px solid #eee',
          fontSize: '12px',
          color: '#666'
        }}>
          <div className="premium-row">
            <span>Session ID:</span>
            <span>{resultData.session_id}</span>
          </div>
          <div className="premium-row">
            <span>Processed At:</span>
            <span>
              {new Date(resultData.processed_at).toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      <button className="btn" onClick={onNewTest}>
        Test Another Scenario
      </button>
    </div>
  );
};

export default ResultPage;