fetch("http://127.0.0.1:5000/upload", { ...
const [extractedData, setExtractedData] = useState(null);

{extractedData && (
  <div>
    <h3>Extracted Resume Data</h3>
    <p><strong>Emails:</strong> {extractedData.emails.join(", ")}</p>
    <p><strong>Names:</strong> {extractedData.names.join(", ")}</p>
    <p><strong>Skills:</strong> {extractedData.skills.join(", ")}</p>
  </div>
)}
