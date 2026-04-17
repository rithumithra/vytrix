import { useNavigate } from "react-router-dom";

export default function Policy() {
  const nav = useNavigate();

  const base = 180;
  const zone = 20;
  const weather = 70;

  const total = base + zone + weather;

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-r from-purple-600 to-blue-500">

      <div className="bg-white p-8 rounded-2xl shadow-lg w-96">
        <h2 className="text-xl font-bold mb-4">Policy & Premium</h2>

        <p>Base: ₹{base}</p>
        <p>Zone Risk: ₹{zone}</p>
        <p>Weather Risk: ₹{weather}</p>

        <h3 className="mt-4 font-bold">Final: ₹{total}</h3>

        <button onClick={()=>nav("/scenario")} className="btn mt-4">
          Activate Plan
        </button>
      </div>
    </div>
  );
}