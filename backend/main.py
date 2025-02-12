from fastapi import FastAPI, UploadFile, File
from backend.utils.resume_parser import parse_resume
from backend.models.ats_scoring import ats_score
from backend.models.skills_extractor import extract_transferable_skills

app = FastAPI()

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), job_description: str = ""):
    """Handles resume upload, text extraction, ATS scoring, and skill extraction."""
    content = await file.read()
    file_type = file.filename.split(".")[-1]

    try:
        resume_text = parse_resume(content, file_type)
        response = {"resume_text": resume_text}

        # ATS Readiness Score
        if job_description:
            response["ats_results"] = ats_score(resume_text, job_description)

        # Transferable Skills Extraction
        response["skills_extracted"] = extract_transferable_skills(resume_text, job_description)

        return response
    except ValueError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
