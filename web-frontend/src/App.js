import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";

function SingleMetricChart({ label, value, unit }) {
  return (
    <div style={{ width: "300px", display: "inline-block", margin: "20px" }}>
      <Bar
        data={{
          labels: [label],
          datasets: [
            {
              label: unit,
              data: [value],
            },
          ],
        }}
        options={{
          scales: {
            y: { beginAtZero: true },
          },
        }}
      />
    </div>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [history, setHistory] = useState([]);
  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzcwNDEzNjM1LCJpYXQiOjE3NzA0MTMzMzUsImp0aSI6IjM0OTVmNTM0ZjA3NjRiMDdhMDgxMmIyYTc1N2E5NWEwIiwidXNlcl9pZCI6IjEifQ.xLcp1hucspKxNRGU1ui4o9BUQYaMAQrKz1wftUYHjAU";

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


// useEffect(() => {
//   fetch("http://localhost:8000/api/history/")
//     .then(res => res.json())
//     .then(data => setHistory(data)); // ✅ data IS the array
// }, []);

useEffect(() => {
  fetch("http://localhost:8000/api/history/",{
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
    .then(res => res.json())
    .then(data => {
      console.log("API DATA:", data);
      setHistory(Array.isArray(data) ? data : []);
    })
    .catch(err => {
      console.error(err);
      setHistory([]);
    });
}, [token]);

  return (
    <div>
      <h1>Equipment Visualizer</h1>

      <input
        type="file"
        accept=".csv"
        onChange={e => setFile(e.target.files[0])}
      />

      <button onClick={upload}>Upload</button>


    {/*TABLE*/}
    {response && response.table && response.table.length > 0 && (
    <>
      <h3>Total Equipment: {response.summary.total_equipment}</h3>

      <table border="1" cellPadding="5">
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
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </>
    )}


{/*Optimised Bar Graphs*/}
{response && response.summary && (
  <>
    <h2>Average Equipment Parameters</h2>

    <SingleMetricChart
      label="Average Flowrate"
      value={response.summary.average_flowrate}
      unit="m³/hr"
    />

    <SingleMetricChart
      label="Average Pressure"
      value={response.summary.average_pressure}
      unit="bar"
    />

    <SingleMetricChart
      label="Average Temperature"
      value={response.summary.average_temperature}
      unit="°C"
    />
  </>
)}


{/*BAR GRAPH*/}
{response?.summary && (
  <Bar
    data={{
      labels: ["Flowrate", "Pressure", "Temperature"],
      datasets: [{
        label: "Average Values",
        data: [
          response.summary.average_flowrate,
          response.summary.average_pressure,
          response.summary.average_temperature,
          ]
        }]
      }}
    />
  )}


      <h3>Upload History</h3>
      {Array.isArray(history) && history.length > 0 ? (
        history.map((item, index) => (
          <div key={index}>
            <strong>{item.filename}</strong>
          </div>
        ))
      ) : (
        <p>No upload history yet.</p>
      )}

    <button onClick={downloadPDF}>Download PDF</button>
    </div>
  );
}

export default App;
