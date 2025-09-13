from fastapi import FastAPI, UploadFile, File
import shutil
import os
from resume_parser import extract_text_from_pdf, extract_text_from_docx, parse_resume

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/extract")
async def extract_resume(file: UploadFile = File(...)):
    # File ko save karna
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # File type check
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file format"}

    # Resume parsing
    parsed = parse_resume(text)

    return {
        "filename": file.filename,
        "parsed_data": parsed
    }
