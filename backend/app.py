from fastapi import FastAPI
from routes import resume

app = FastAPI()

# include routes
app.include_router(resume.router)

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully 🚀"}

