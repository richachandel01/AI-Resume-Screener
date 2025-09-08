// src/ResumeUploader.jsx
import React, { useState } from "react";

export default function ResumeUploader(){
  const [status, setStatus] = useState("");
  const [result, setResult] = useState(null);

  const onUpload = async () => {
    const input = document.getElementById("file");
    if(!input || !input.files[0]) { setStatus("Choose a file"); return; }
    setStatus("Uploading...");
    const fd = new FormData();
    fd.append("file", input.files[0]);

    try{
      const res = await fetch("http://127.0.0.1:5001/upload", { method: "POST", body: fd });
      const data = await res.json();
      if(!res.ok) throw new Error(JSON.stringify(data));
      setResult(data);
      setStatus("Upload complete");
    }catch(err){
      setStatus("Error: " + err.message);
    }
  }

  return (
    <div>
      <input id="file" type="file" accept=".pdf,.docx" />
      <button onClick={onUpload}>Upload Resume</button>
      <div>{status}</div>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
