import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Register() {
  const nav = useNavigate();

  const [form, setForm] = useState({
    name: "",
    phone: "",
    zone: "",
    start_time: "",
    end_time: "",
    earnings: ""
  });


  const handleSubmit = async () => {

    // ✅ ADD THIS BLOCK HERE
    if (!form.zone) {
      alert("Please select a valid city");
      return;
    }

    try {
      const res = await fetch("https://vytrix-backend.onrender.com/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          ...form,
          earnings: Number(form.earnings)  // 🔥 important fix
        })
      });

      const data = await res.json();

      const updatedUser = {
        ...form,
        user_id: data.user_id
      };

      localStorage.setItem("user", JSON.stringify(updatedUser));

      nav("/dashboard");

    } catch (err) {
      console.error("ERROR:", err);
      alert("Backend not connected!");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-r from-purple-600 to-blue-500">

      <div className="bg-white p-8 rounded-2xl shadow-lg w-96">

        <h2 className="text-xl font-bold mb-4 text-center">Register</h2>

        <input
          placeholder="Name"
          className="input"
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        <input
          placeholder="Phone"
          className="input"
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />

        {/* CITY */}
        <select
          className="input"
          onChange={(e) => setForm({ ...form, zone: e.target.value })}
        >
          <option value="">Select City</option>   {/* FIX */}
          <option value="Hyderabad">Hyderabad</option>
          <option value="Bengaluru">Bengaluru</option>
          <option value="Mumbai">Mumbai</option>
          <option value="Delhi">Delhi</option>
        </select>

        {/* TIME IN ONE LINE 🔥 */}
        <div className="flex gap-4 mb-3">
          <input
            type="time"
            className="input flex-1"
            onChange={(e) => setForm({ ...form, start_time: e.target.value })}
          />
          <input
            type="time"
            className="input flex-1"
            onChange={(e) => setForm({ ...form, end_time: e.target.value })}
          />
        </div>

        <input
          placeholder="Daily Earnings ₹"
          className="input"
          onChange={(e) => setForm({ ...form, earnings: e.target.value })}
        />

        <button onClick={handleSubmit} className="btn">
          Continue
        </button>

      </div>
    </div>
  );
}
