import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setMessage(data.message || "File uploaded successfully!");
    } catch (error) {
      setMessage("Upload failed. Check backend server.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Resume Screener</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload Resume</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
