// src/App.js
import React from "react";
import ResumeUploader from "./ResumeUploader"; // agar file ka path alag ho to change karo

function App(){
  return (
    <div style={{padding:20}}>
      <h1>AI Resume Screener</h1>
      <ResumeUploader />
    </div>
  )
}

export default App;
