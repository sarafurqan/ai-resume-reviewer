import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

def check_formatting(resume_text):
    """Checks if the resume has proper formatting."""
    sections = ["experience", "education", "skills", "projects", "certifications"]
    missing_sections = [sec for sec in sections if sec.lower() not in resume_text.lower()]
    return {"missing_sections": missing_sections}

def keyword_match(resume_text, job_description):
    """Matches keywords between the resume and job description."""
    vectorizer = TfidfVectorizer(stop_words="english")
    docs = [resume_text, job_description]
    tfidf_matrix = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()
    
    resume_keywords = Counter(re.findall(r"\b\w+\b", resume_text.lower()))
    job_keywords = Counter(re.findall(r"\b\w+\b", job_description.lower()))
    
    matched_keywords = set(resume_keywords.keys()) & set(job_keywords.keys())
    match_score = len(matched_keywords) / len(set(job_keywords.keys())) * 100
    return {"match_score": round(match_score, 2), "matched_keywords": list(matched_keywords)}

def ats_score(resume_text, job_description):
    """Calculates an ATS score based on formatting and keyword match."""
    formatting_issues = check_formatting(resume_text)
    keyword_analysis = keyword_match(resume_text, job_description)

    score = (100 - (len(formatting_issues["missing_sections"]) * 10)) + keyword_analysis["match_score"]
    return {"ats_score": round(score / 2, 2), "formatting_issues": formatting_issues, "keyword_analysis": keyword_analysis}
