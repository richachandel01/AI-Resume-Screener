import React, { useState } from "react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:5000";
console.log("BACKEND_URL:", BACKEND_URL);

export default function UploadResume({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [extractedData, setExtractedData] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage("");
    setExtractedData(null);
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file) {
      setMessage("Choose a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      setMessage("Uploading...");
      const response = await fetch(`${BACKEND_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(\`Server responded \${response.status}: \${errText}\`);
      }

      const data = await response.json();
      console.log("Upload response:", data);
      setMessage("Upload successful!");
      const parsed = data.data ?? data;
      setExtractedData(parsed);
      if (onUploadSuccess) onUploadSuccess(parsed, data.resume_id ?? data.resumeId);
    } catch (error) {
      console.error("Error uploading file:", error);
      const errMsg = error.message || "Upload failed";
      if (errMsg.includes("Failed to fetch") || errMsg.includes("NetworkError")) {
        setMessage("Upload failed: could not reach backend. Is it running on port 5000?");
      } else {
        setMessage("Upload failed: " + errMsg);
      }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-card">
      <h2>Upload Resume</h2>
      <form onSubmit={handleUpload}>
        <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} />
        <button type="submit" disabled={uploading}>
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </form>
      <p className="message">{message}</p>

      {extractedData && (
        <div className="results-card">
          <h3>Extracted Resume Data</h3>
          <p><strong>Emails:</strong> {(extractedData.emails || []).join(", ") || "—"}</p>
          <p><strong>Names:</strong> {(extractedData.names || []).join(", ") || "—"}</p>
          <p><strong>Skills:</strong> {(extractedData.skills || []).join(", ") || "—"}</p>
          <p><strong>Phone:</strong> {(extractedData.phones || []).join(", ") || "—"}</p>
          {extractedData.resume_id && (
            <p>
              <a href={\`\${BACKEND_URL}/resumes/\${extractedData.resume_id}\`} target="_blank" rel="noreferrer">
                View saved resume
              </a>
            </p>
          )}
        </div>
      )}
    </div>
  );
}
