// import { useState } from "react";
// import API_BASE_URL from "./utils/config";

// export default function Login({ setToken }) {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [error, setError] = useState("");

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     setError("");

//     try {
//       const res = await fetch(`${API_BASE_URL}/api/token/`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ username, password }),
//       });

//       if (!res.ok) {
//         setError("Login failed. Check username/password.");
//         return;
//       }

//       const data = await res.json();
//       setToken(data.access); // store the JWT token in parent App state
//     } catch (err) {
//       setError("Network error.");
//     }
//   };

//   return (
//     <form onSubmit={handleLogin} style={{ textAlign: "center", marginTop: "50px" }}>
//       <h2>Login</h2>
//       <input
//         type="text"
//         placeholder="Username"
//         value={username}
//         onChange={(e) => setUsername(e.target.value)}
//         required
//         style={{ padding: "5px", margin: "5px" }}
//       />
//       <input
//         type="password"
//         placeholder="Password"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//         required
//         style={{ padding: "5px", margin: "5px" }}
//       />
//       <br />
//       <button type="submit" style={{ padding: "5px 15px", marginTop: "10px" }}>
//         Login
//       </button>
//       {error && <p style={{ color: "red" }}>{error}</p>}
//     </form>
//   );
// }

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
