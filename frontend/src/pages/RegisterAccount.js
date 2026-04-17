import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function RegisterAccount() {
  const nav = useNavigate();

  const [form, setForm] = useState({});
  const [otpSent, setOtpSent] = useState(false);

  // 🔥 SEND OTP
  const sendOtp = async () => {
    if (!form.email) {
      alert("Enter email first");
      return;
    }

    try {
      const res = await fetch("https://vytrix-backend.onrender.com/send_otp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: form.email
        })
      });

      const data = await res.json();

      // 🔥 THIS IS THE IMPORTANT LINE
      alert("Your OTP is: " + data.otp);

      setOtpSent(true);

    } catch (err) {
      console.error(err);
      alert("Backend not connected!");
    }
  };
  // 🔥 VERIFY OTP + CREATE ACCOUNT
  const verifyOtp = async () => {
    const res = await fetch("https://vytrix-backend.onrender.com/verify_otp", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    const data = await res.json();

    if (data.status === "success") {
      alert("Account created successfully!");
      nav("/");
    } else {
      alert("Wrong OTP");
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-r from-purple-600 to-blue-500">

      <div className="bg-white p-8 rounded-2xl shadow-lg w-80">

        <h2 className="text-xl font-bold mb-4 text-center">
          Register Account
        </h2>

        {/* NAME */}
        <input
          placeholder="Name"
          className="input"
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        {/* PHONE */}
        <input
          placeholder="Phone"
          className="input"
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />

        {/* EMAIL */}
        <input
          placeholder="Email"
          className="input"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        {/* PASSWORD */}
        <input
          placeholder="Password"
          type="password"
          className="input"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        {/* 🔥 BEFORE OTP */}
        {!otpSent ? (
          <button onClick={sendOtp} className="btn">
            Send OTP
          </button>
        ) : (
          <>
            {/* OTP INPUT */}
            <input
              placeholder="Enter OTP"
              className="input"
              onChange={(e) => setForm({ ...form, otp: e.target.value })}
            />

            <button onClick={verifyOtp} className="btn">
              Verify & Register
            </button>
          </>
        )}

        <p
          className="text-center mt-3 cursor-pointer text-blue-500"
          onClick={() => nav("/")}
        >
          Back to Login
        </p>

      </div>
    </div>
  );
}
