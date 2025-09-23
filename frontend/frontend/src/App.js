const handleUpload = async (event) => {
  event.preventDefault();
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:5002/extract", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Extracted data:", data);
    setMessage("Upload successful!");
    setExtractedData(data);  // store the extracted info
  } catch (error) {
    console.error("Error uploading file:", error);
    setMessage("Upload failed");
  }
};

