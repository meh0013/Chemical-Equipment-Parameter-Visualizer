import logo from './logo.svg';
import './App.css';
import { useState } from "react";
import axios from "axios";


function App() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const upload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData
    );

    setResponse(res.data);
  };

  return (
    <div>
      <h1>Equipment Visualizer</h1>

      <input
        type="file"
        accept=".csv"
        onChange={e => setFile(e.target.files[0])}
      />

      <button onClick={upload}>Upload</button>

      <pre>{JSON.stringify(response, null, 2)}</pre>
    </div>
  );
}

export default App;
