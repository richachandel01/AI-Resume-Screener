from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "NLP Service Running 🚀"}

@app.post("/process_resume/")
async def process_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    # Dummy skill extraction
    skills = []
    for skill in ["Python", "Java", "C++", "SQL", "AWS", "React", "Flask"]:
        if skill.lower() in text.lower():
            skills.append(skill)

    return {
        "filename": file.filename,
        "skills": skills,
        "summary": f"Extracted {len(skills)} skills"
    }
