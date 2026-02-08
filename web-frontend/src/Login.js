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
        setError("Login failed. Check username/password.");
        return;
      }

      const data = await res.json();
      setToken(data.access); // store the JWT token in parent App state
    } catch (err) {
      setError("Network error.");
    }
  };

  return (
    <form onSubmit={handleLogin} style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        style={{ padding: "5px", margin: "5px" }}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        style={{ padding: "5px", margin: "5px" }}
      />
      <br />
      <button type="submit" style={{ padding: "5px 15px", marginTop: "10px" }}>
        Login
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}
