import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import UploadResume from "./pages/UploadResume";

function App() {
  return (
    <Router>
      <div className="p-6">
        <nav className="mb-4">
          <Link to="/" className="mr-4">Home</Link>
          <Link to="/upload">Upload Resume</Link>
        </nav>

        <Routes>
          <Route path="/" element={<h1 className="text-2xl">Welcome to AI Resume Screener</h1>} />
          <Route path="/upload" element={<UploadResume />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
