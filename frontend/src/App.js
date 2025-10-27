import React from "react";
import UploadResume from "./components/UploadResume";
import "./App.css";

function App() {
  return (
    <div style={{ padding: "1.5rem" }}>
      <h1>AI Resume Screener — Frontend Smoke Test</h1>
      <UploadResume />
    </div>
  );
}

export default App;
