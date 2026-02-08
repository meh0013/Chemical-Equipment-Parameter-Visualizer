import { useState } from "react";
import API_BASE_URL from "./utils/config";

export default function Login({ setToken }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await fetch(`${API_BASE_URL}/api/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        setError("Invalid username or password");
        return;
      }

      const data = await res.json();
      setToken(data.access);
    } catch (err) {
      setError("Unable to connect to server");
    }
  };

  return (
    <div className="login-container">
      <h2>Equipment Visualizer</h2>
      <p style={{ textAlign: "center", marginBottom: "20px", color: "#666" }}>
        Please log in to continue
      </p>

      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Login</button>

        {error && (
          <p style={{ color: "#e74c3c", marginTop: "15px", textAlign: "center" }}>
            {error}
          </p>
        )}
      </form>
    </div>
  );
}
