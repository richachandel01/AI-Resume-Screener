from fastapi import FastAPI, File, UploadFile
import pdfplumber

app = FastAPI()

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    """
    Extract text from uploaded PDF file.
    """
    try:
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}
