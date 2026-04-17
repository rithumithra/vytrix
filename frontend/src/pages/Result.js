export default function Result() {
  const data = JSON.parse(localStorage.getItem("result"));
  const user = JSON.parse(localStorage.getItem("user"));

  const getDecisionColor = () => {
    if (data.decision === "APPROVED") return "text-green-400";
    if (data.decision === "VERIFY") return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-br from-black via-gray-900 to-black">

      <div className="bg-white/5 backdrop-blur-lg border border-yellow-500/20 p-10 rounded-3xl shadow-2xl w-[420px] text-white">

        <h2 className="text-2xl font-bold text-yellow-400 mb-4 text-center">
          Claim Result
        </h2>

        {/* Scores */}
        <p className="text-sm">Opportunity Score: {data.opportunity_score}</p>
        <p className="text-sm mb-3">Fraud Score: {data.fraud_score}</p>

        {/* Weather */}
        <div className="mb-4 text-sm">
          <h4 className="font-bold text-yellow-300">Weather Conditions:</h4>
          <p>🌧 Rain: {data.weather?.rain || 0} mm</p>
          <p>🌡 Temperature: {data.weather?.temp || 0} °C</p>
        </div>

        {/* Bars */}
        <div className="mb-4">
          <p className="text-xs">Opportunity Score</p>
          <div className="bg-gray-800 h-2 rounded">
            <div
              className="bg-yellow-400 h-2 rounded"
              style={{ width: `${data.opportunity_score * 100}%` }}
            ></div>
          </div>

          <p className="text-xs mt-2">Fraud Score</p>
          <div className="bg-gray-800 h-2 rounded">
            <div
              className="bg-red-500 h-2 rounded"
              style={{ width: `${data.fraud_score * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Decision */}
        <h3 className={`text-xl font-bold ${getDecisionColor()}`}>
          {data.decision}
        </h3>

        {/* Reasons */}
        <div className="mt-4 text-sm">
          <h4 className="font-bold text-yellow-300">Decision Factors:</h4>

          {data.weather?.temp > 35 && <p>• High temperature affecting delivery</p>}
          {data.weather?.rain > 5 && <p>• Heavy rainfall disruption</p>}
          {data.opportunity_score > 0.6 && <p>• Opportunity loss detected</p>}
          {data.fraud_score > 0.5 && <p>• Suspicious behavior detected</p>}
          {data.fraud_score > 0.8 && <p>• High fraud risk identified</p>}
        </div>

        {/* AI line */}
        <p className="text-gray-400 text-xs mt-3">
          Decision generated using real-time environmental and behavioral analysis
        </p>

        {/* 💸 Payout */}
        {data.decision === "APPROVED" && (
          <div className="mt-4 text-green-400 font-bold text-sm">
            💸 Instant payout of ₹{data.payout} processed via UPI (simulated)
            <p className="text-gray-400 text-xs mt-1">
              Transaction ID: {data.transaction_id}
            </p>
          </div>
        )}

      </div>
    </div>
  );
}