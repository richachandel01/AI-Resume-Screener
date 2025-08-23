import React, { useState } from "react";

function UploadResume() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5002/process_resume/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Your Resume</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      {response && (
        <div className="result">
          <h3>Analysis Result</h3>
          <p><strong>Filename:</strong> {response.filename}</p>
          <p><strong>Skills:</strong> {response.skills.join(", ")}</p>
          <p><strong>Summary:</strong> {response.summary}</p>
        </div>
      )}
    </div>
  );
}

export default UploadResume;
