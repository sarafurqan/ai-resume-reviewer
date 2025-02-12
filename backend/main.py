from fastapi import FastAPI, UploadFile, File
from backend.utils.resume_parser import parse_resume
from backend.models.ats_scoring import ats_score

app = FastAPI()

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), job_description: str = ""):
    """Handles resume upload, text extraction, and ATS scoring."""
    content = await file.read()
    file_type = file.filename.split(".")[-1]

    try:
        resume_text = parse_resume(content, file_type)
        if job_description:
            ats_results = ats_score(resume_text, job_description)
            return {"resume_text": resume_text, "ats_results": ats_results}
        return {"resume_text": resume_text}
    except ValueError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
