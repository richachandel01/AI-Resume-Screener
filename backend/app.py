from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def root():
    return {"message": "AI Resume Screener backend is running!"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # file key ka naam exactly "file" hona chahiye (Postman me bhi yahi use hoga)
    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        f.write(await file.read())

    size = save_path.stat().st_size
    return JSONResponse({
        "message": "File uploaded",
        "filename": file.filename,
        "size": size,
        "saved_path": str(save_path.resolve())
    })
