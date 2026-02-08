import "./App.css";
import axios from "axios";
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";
import Login from "./Login";
import API_BASE_URL from "./utils/config";

function SingleMetricChart({ label, value, unit, color }) {
  return (
    <div className="card metric-card">
      <h4>{label}</h4>
      <Bar
        data={{
          labels: [label],
          datasets: [
            {
              data: [value],
              backgroundColor: color,
            },
          ],
        }}
        options={{
          scales: { y: { beginAtZero: true } },
          plugins: { legend: { display: false } },
        }}
      />
      <p className="metric-value">
        {value} {unit}
      </p>
    </div>
  );
}

function App() {
  const [token, setToken] = useState("");
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE_URL}/api/history/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setHistory(Array.isArray(data) ? data : []))
      .catch(() => setHistory([]));
  }, [token]);

  if (!token) return <Login setToken={setToken} />;

  const upload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      `${API_BASE_URL}/api/upload/`,
      formData,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    setResponse(res.data);
  };

  const downloadPDF = () => {
    if (!response?.summary) {
      alert("No summary to download");
      return;
    }

    fetch(`${API_BASE_URL}/api/pdf/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ summary: response.summary }),
    })
      .then((res) => res.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "report.pdf";
        a.click();
        window.URL.revokeObjectURL(url);
      });
  };

  return (
    <div className="app-background">
      <div className="app-container">
        <header className="app-header">
          <h1>Equipment Visualizer</h1>
          <p>Upload CSV · Analyze Metrics · Export PDF</p>
        </header>

        {/* Upload Controls */}
        <div className="card controls">
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button className="primary" onClick={upload}>
            Upload CSV
          </button>
          <button className="secondary" onClick={downloadPDF}>
            Download PDF
          </button>
        </div>

        {/* Summary Table */}
        {response?.table?.length > 0 && (
          <div className="card">
            <h2>Summary Table</h2>
            <p>
              <strong>Total Equipment:</strong>{" "}
              {response.summary.total_equipment}
            </p>

            <table className="styled-table">
              <thead>
                <tr>
                  {Object.keys(response.table[0]).map((key) => (
                    <th key={key}>{key}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {response.table.map((row, idx) => (
                  <tr key={idx}>
                    {Object.values(row).map((val, i) => (
                      <td key={i}>{val}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Metric Cards */}
        {response?.summary && (
          <>
            <h2 className="section-title">Average Equipment Metrics</h2>

            <div className="metrics-grid">
              <SingleMetricChart
                label="Flowrate"
                value={response.summary.average_flowrate}
                unit="m³/hr"
                color="#4caf50"
              />
              <SingleMetricChart
                label="Pressure"
                value={response.summary.average_pressure}
                unit="bar"
                color="#2196f3"
              />
              <SingleMetricChart
                label="Temperature"
                value={response.summary.average_temperature}
                unit="°C"
                color="#ff9800"
              />
            </div>

            {/* Combined Chart */}
            <div className="card">
              <h3>Combined Metrics</h3>
              <Bar
                data={{
                  labels: ["Flowrate", "Pressure", "Temperature"],
                  datasets: [
                    {
                      data: [
                        response.summary.average_flowrate,
                        response.summary.average_pressure,
                        response.summary.average_temperature,
                      ],
                      backgroundColor: ["#4caf50", "#2196f3", "#ff9800"],
                    },
                  ],
                }}
                options={{ scales: { y: { beginAtZero: true } } }}
              />
            </div>
          </>
        )}

        {/* History */}
        <div className="card">
          <h2>Upload History</h2>
          {history.length > 0 ? (
            <ul className="history-list">
              {history.map((item, idx) => (
                <li key={idx}>
                  <strong>{item.filename}</strong>
                  <span>
                    {new Date(item.uploaded_at).toLocaleString()}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p>No uploads yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
