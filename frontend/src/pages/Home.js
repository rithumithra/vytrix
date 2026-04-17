import { useNavigate } from "react-router-dom";

export default function Home() {
  const nav = useNavigate();

  return (
    <div style={{
      height: "100vh",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      background: "linear-gradient(to right, purple, blue)",
      color: "white"
    }}>
      <h1>Vytrix</h1>
      <p>AI Powered Income Protection</p>

      <button onClick={() => nav("/dashboard")}>
        Get Started
      </button>
    </div>
  );
}