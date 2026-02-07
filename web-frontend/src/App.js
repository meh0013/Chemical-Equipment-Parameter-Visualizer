import './App.css';
import axios from "axios";
import { useEffect, useState } from "react";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";
import Login from "./Login";

//Chart
function SingleMetricChart({ label, value, unit }) {
  return (
    <div style={{ 
        width: "250px",
        display: "inline-block",
        margin: "10px",
        padding: "15px",
        boxShadow: "0 0 10px #d3d3d3",
        borderRadius: "10px",
        textAlign: "center",
        backgroundColor: "#FFFFFF",
      }}>
      <h4>{label}</h4>
      <Bar
        data={{
          labels: [label],
          datasets: [
            {
              label: unit,
              data: [value],
              backgroundColor: "#4caf50",
            },
          ],
        }}
        options={{
          scales: { y: { beginAtZero: true } },
          plugins: { legend: { display: false } },
        }}
      />
      <p style={{ marginTop: "10px", fontWeight: "bold" }}>
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
    if (!token) return; // safe: skip fetching if no token yet

    fetch("http://localhost:8000/api/history/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
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
      "http://127.0.0.1:8000/api/upload/",
      formData,
      {
        headers:{
          Authorization: `Bearer ${token}`
        }
      }
    );

    setResponse(res.data);
  };

  const downloadPDF = () => {
    if (!response?.summary) {
      alert("No summary to download");
      return;
    }

    fetch("http://localhost:8000/api/pdf/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify({ summary: response.summary }),
    })
      .then(res => res.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "report.pdf";
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch(err => {
        console.error("PDF download failed:", err);
      });
  };

return (
    <div style={{ maxWidth: "1000px", margin: "auto", fontFamily: "Arial, sans-serif", padding: "20px" }}>
      <header style={{ textAlign: "center", marginBottom: "30px" }}>
        <h1>Equipment Visualizer</h1>
        <p>Upload CSV, view metrics, history, and download PDF report</p>
      </header>

      {/* Upload Section */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginRight: "10px" }}
        />
        <button onClick={upload} style={{ padding: "5px 15px", marginRight: "10px" }}>
          Upload
        </button>
        <button onClick={downloadPDF} style={{ padding: "5px 15px" }}>
          Download PDF
        </button>
      </div>

      {/* Table */}
      {response?.table && response.table.length > 0 && (
        <div style={{ marginBottom: "30px" }}>
          <h2>Summary Table</h2>
          <h4>Total Equipment: {response.summary.total_equipment}</h4>
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              marginBottom: "20px",
            }}
          >
            <thead style={{ backgroundColor: "#ffffff" }}>
              <tr>
                {Object.keys(response.table[0]).map((key) => (
                  <th key={key} style={{ border: "1px solid #dedbdb", padding: "8px" }}>
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {response.table.map((row, idx) => (
                <tr key={idx}>
                  {Object.values(row).map((val, i) => (
                    <td key={i} style={{ border: "1px solid #dedbdb", padding: "8px" }}>
                      {val}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Individual Metric Charts */}
      {response?.summary && (
        <>
          <h2>Average Equipment Metrics</h2>
          <div>
            <SingleMetricChart
              label="Flowrate"
              value={response.summary.average_flowrate}
              unit="m³/hr"
            />
            <SingleMetricChart
              label="Pressure"
              value={response.summary.average_pressure}
              unit="bar"
            />
            <SingleMetricChart
              label="Temperature"
              value={response.summary.average_temperature}
              unit="°C"
            />
          </div>

          {/* Combined Bar Chart */}
          <div style={{ marginTop: "20px" }}>
            <h3>Combined Metrics</h3>
            <Bar
              data={{
                labels: ["Flowrate", "Pressure", "Temperature"],
                datasets: [
                  {
                    label: "Average Values",
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

      {/* Upload History */}
      <div style={{ marginTop: "30px" }}>
        <h2>Upload History (Last 5)</h2>
        {history.length > 0 ? (
          <ul style={{ listStyle: "none", padding: 0 }}>
            {history.map((item, idx) => (
              <li
                key={idx}
                style={{
                  padding: "8px",
                  marginBottom: "5px",
                  border: "1px solid #dedbdb",
                  borderRadius: "5px",
                  backgroundColor: "#ffffff",
                }}
              >
                <strong>{item.filename}</strong>{" "}
                <span style={{ color: "#727171", fontSize: "1em" }}>
                  ({new Date(item.uploaded_at).toLocaleString()})
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p>No uploads yet.</p>
        )}
      </div>
    </div>
  );
}

export default App;