import { useNavigate } from "react-router-dom";

export default function Scenario() {
  const nav = useNavigate();

  const user = JSON.parse(localStorage.getItem("user"));

  if (!user) {
    alert("Please login first!");
    window.location.href = "/";
  }

  const simulate = async (type) => {
    try {
      const res = await fetch("https://vytrix-backend.onrender.com/claim", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: user.user_id,
          scenario: type
        })
      });

      const data = await res.json();
      localStorage.setItem("result", JSON.stringify(data));
      nav("/result");

    } catch (err) {
      console.error("ERROR:", err);
      alert("Claim API not working!");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-br from-black via-gray-900 to-black">

      {/* 🔥 CARD */}
      <div className="bg-white/5 backdrop-blur-lg border border-yellow-500/20 p-10 rounded-3xl shadow-2xl w-[400px] text-center">

        {/* Title */}
        <h2 className="text-2xl font-bold text-yellow-400 mb-2">
          Test Scenario
        </h2>

        <p className="text-gray-400 mb-6 text-sm">
          Simulate real-world disruptions and test AI decisions
        </p>

        {/* 🌧 RAIN */}
        <button
          onClick={() => simulate("rain")}
          className="w-full bg-yellow-500 text-black py-3 rounded-xl mb-4 hover:bg-yellow-400 hover:scale-105 transition duration-300 font-semibold shadow-lg"
        >
          🌧 Simulate Heavy Rain
        </button>

        {/* 🚫 FRAUD */}
        <button
          onClick={() => simulate("fraud")}
          className="w-full bg-red-500 text-white py-3 rounded-xl mb-4 hover:bg-red-400 hover:scale-105 transition duration-300 font-semibold shadow-lg"
        >
          🚫 Simulate Fraud
        </button>

        {/* ⚡ NORMAL */}
        <button
          onClick={() => simulate("normal")}
          className="w-full bg-gray-800 text-yellow-300 py-3 rounded-xl hover:bg-gray-700 hover:scale-105 transition duration-300 font-semibold"
        >
          ⚡ Normal Scenario
        </button>

      </div>
    </div>
  );
}
