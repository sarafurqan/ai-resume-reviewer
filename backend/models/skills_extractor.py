import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

# Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Predefined Skill Lists (Expand as Needed)
HARD_SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data analysis", "sql", "fastapi", "django", "tensorflow",
    "nlp", "cloud computing", "cybersecurity", "big data"
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "adaptability", "creativity", "work ethic",
    "time management", "collaboration", "conflict resolution"
]

def extract_skills_using_nlp(text):
    """Extracts potential skills from the resume using NLP."""
    doc = nlp(text.lower())
    skills = set()
    
    for token in doc:
        if token.text in HARD_SKILLS or token.text in SOFT_SKILLS:
            skills.add(token.text)
    
    return list(skills)

def extract_skills_using_tfidf(resume_text, job_description):
    """Finds keyword matches between resume and job description using TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words="english")
    docs = [resume_text, job_description]
    tfidf_matrix = vectorizer.fit_transform(docs)
    
    feature_names = vectorizer.get_feature_names_out()
    
    resume_words = Counter(re.findall(r"\b\w+\b", resume_text.lower()))
    job_words = Counter(re.findall(r"\b\w+\b", job_description.lower()))
    
    matched_skills = set(resume_words.keys()) & set(job_words.keys())
    return list(matched_skills)

def extract_transferable_skills(resume_text, job_description=""):
    """Extracts transferable skills using NLP and TF-IDF methods."""
    nlp_skills = extract_skills_using_nlp(resume_text)
    
    if job_description:
        tfidf_skills = extract_skills_using_tfidf(resume_text, job_description)
        all_skills = list(set(nlp_skills + tfidf_skills))
    else:
        all_skills = nlp_skills

    return {"skills_extracted": all_skills}
