import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";                 // 🔥 NEW
import RegisterAccount from "./pages/RegisterAccount"; // 🔥 NEW
import Profile from "./pages/Profile";             // 🔥 NEW

import Policy from "./pages/Policy";               // keep if needed
import Scenario from "./pages/Scenario";
import Result from "./pages/Result";

import Dashboard from "./pages/Dashboard";
import Trust from "./pages/Trust";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 🔐 AUTH FLOW */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<RegisterAccount />} />
        <Route path="/profile" element={<Profile />} />

        {/* EXISTING */}
        <Route path="/policy" element={<Policy />} />
        <Route path="/scenario" element={<Scenario />} />
        <Route path="/result" element={<Result />} />

        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/trust" element={<Trust />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;