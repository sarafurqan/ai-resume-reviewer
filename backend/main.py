from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from backend.utils.resume_parser import parse_resume
from backend.models.ats_scoring import ats_score
from backend.models.skills_extractor import extract_transferable_skills

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend to access API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), job_description: str = ""):
    """Handles resume upload, text extraction, ATS readiness scoring, and transferable skills extraction."""

    try:
        content = await file.read()
        file_type = file.filename.split(".")[-1]

        # Process resume text
        resume_text = parse_resume(content, file_type)
        ats_results = ats_score(resume_text, job_description) if job_description else None
        skills_extracted = extract_transferable_skills(resume_text, job_description)

        return JSONResponse(content={
            "resume_text": resume_text,
            "ats_results": ats_results,
            "skills_extracted": skills_extracted
        }, media_type="application/json")
    except ValueError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
