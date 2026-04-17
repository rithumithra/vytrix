import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const nav = useNavigate();
  const [form, setForm] = useState({});

  const login = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      const data = await res.json();

      console.log(data);   // 🔥 DEBUG

      if (data.status === "success") {
        alert("Login success");
        localStorage.setItem("user", JSON.stringify(data));
        nav("/dashboard");
      } else {
        alert("Login failed");
      }

    } catch (err) {
      console.error(err);
      alert("Backend error");
    }
  };

  return (
    <div
      className="min-h-screen bg-cover bg-center flex items-center justify-end pr-24 relative"
      style={{
        backgroundImage:
          "url('https://images.openai.com/static-rsc-4/33tnE-qSnEDpB-iZM_hv4hK-6hvYcpYi8rfC1hPySGscXLMmkObAdot-xnB_lCyJSZKKI97MELjnL8OYfMdzLbe5Kbkr5wmbfVOExtuVWWOrU2uxTULFDgAtX7nZk7GQUppBQRjXIFFEG3Fc1vIQdHGW4GRqlm__XWqV6iD_1e1-sQgq7uuW-0ZVovm1-2MF?purpose=fullsize')"
      }}
    >

      {/* 🔥 Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-50"></div>

      {/* 🔥 LOGIN CARD */}
      <div className="relative z-10 bg-white p-10 rounded-3xl shadow-2xl w-[380px]">

        <h1 className="text-3xl font-bold text-center mb-2 text-yellow-600">
          VYTRIX
        </h1>

        <h2 className="text-lg font-semibold mb-6 text-center text-gray-700">
          Login to continue
        </h2>

        {/* Email */}
        <input
          placeholder="Email"
          className="w-full border border-gray-300 p-3 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        {/* Password */}
        <input
          placeholder="Password"
          type="password"
          className="w-full border border-gray-300 p-3 rounded-lg mb-5 focus:outline-none focus:ring-2 focus:ring-purple-500"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        {/* Button */}
        <button
          onClick={login}
          className="w-full bg-gradient-to-r from-yellow-600 to-red-500 text-white py-3 rounded-lg hover:scale-105 transition duration-300 shadow-lg"
        >
          Login
        </button>

        {/* Register */}
        <p
          className="text-center mt-4 cursor-pointer text-blue-500 hover:underline"
          onClick={() => nav("/register")}
        >
          Create Account
        </p>

      </div>
    </div>
  );
}