import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const nav = useNavigate();

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-center relative"
      style={{
        backgroundImage:
          "url('https://images.openai.com/static-rsc-4/cpPDi-CgJ6qYfnCNaSirwAJ1f4oJ5AlWugtweDGFOXaleSb9AsPTQg67y33BiPekmpRzs6taj7lEuPCp9VI2GgCUzInZYspLpiDZ_B6yZ9zuBTi2lrZ4F5Kb8J3rMOo8PcGN4ggS6k-Gr8tYIPVHSl2OiYUF4wk536FIYNKoY3C3Qx1a7WqagKb0mZTmsrQE?purpose=fullsize')"
      }}
    >
      {/* 🔥 Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-60"></div>

      {/* 🔥 Main Card */}
      <div className="relative z-10 bg-white/10 backdrop-blur-lg p-10 rounded-3xl shadow-2xl border border-white/20 w-[420px] text-white">

        {/* Title */}
        <h1 className="text-3xl font-bold mb-2 text-center">
          Vytrix Dashboard
        </h1>

        <p className="text-gray-300 text-center mb-6 text-sm">
          AI-powered protection for delivery partners
        </p>

        {/* 🧑 WORKER SECTION */}
        <div className="mb-6">
          <h3 className="font-bold mb-2">🧑 Worker Insights</h3>
          <div className="bg-white/10 p-3 rounded-xl text-sm">
            <p>Earnings Protected: ₹1200</p>
            <p>Active Coverage: Dinner Shift</p>
          </div>
        </div>

        {/* 🏢 INSURER SECTION */}
        <div className="mb-6">
          <h3 className="font-bold mb-2">🏢 Insurer Analytics</h3>
          <div className="bg-white/10 p-3 rounded-xl text-sm">
            <p>Loss Ratio: 32%</p>
            <p>Next Week Risk: HIGH</p>
            <p>Predicted Disruption: Heavy Rain</p>
          </div>
        </div>

        {/* 🚀 BUTTONS */}
        <button onClick={() => nav("/profile")} className="w-full bg-gradient-to-r from-yellow-600 to-black-500 text-white py-3 rounded-xl mb-4 hover:scale-105 transition duration-300 shadow-lg" >
          🚀 Claim Insurance
        </button>
        {/* ⭐ Trust Score */}
        <button onClick={() => nav("/trust")} className="w-full bg-red text-red-600 py-3 rounded-xl hover:bg-gray-100 transition duration-300 shadow">

          ⭐ View Trust Score </button> <button onClick={() => nav("/scenario")} className="w-full bg-red-500 text-red py-3 rounded-xl mb-4 hover:scale-105 transition duration-300" > 📊 Run Simulation </button> </div> </div>);
}