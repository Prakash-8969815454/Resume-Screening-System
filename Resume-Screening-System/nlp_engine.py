import re
from typing import List, Dict, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Standard skills taxonomy dictionary
COMMON_SKILLS = {
    "python", "java", "c++", "javascript", "typescript", "html", "css", "react", 
    "angular", "vue", "node.js", "fastapi", "django", "flask", "sql", "postgresql", 
    "mysql", "mongodb", "docker", "kubernetes", "aws", "azure", "git", "github", 
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "pandas", 
    "numpy", "scikit-learn", "rest api", "graphql", "agile", "devops", "ci/cd"
}

def extract_email(text: str) -> str:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, text)
    return match.group(0) if match else "N/A"

def extract_phone(text: str) -> str:
    pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(pattern, text)
    return match.group(0) if match else "N/A"

def extract_skills(text: str) -> Set[str]:
    text_lower = text.lower()
    found_skills = set()
    for skill in COMMON_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill.capitalize())
    return found_skills

def calculate_match_score(resume_text: str, job_description: str) -> Dict:
    """Calculates TF-IDF Cosine Similarity and skill overlaps."""
    documents = [resume_text, job_description]
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Cosine Similarity Calculation
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    match_percentage = round(float(similarity_matrix[0][0]) * 100, 2)
    
    # Skill Overlap Analysis
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)
    
    matched_skills = list(resume_skills.intersection(jd_skills))
    missing_skills = list(jd_skills.difference(resume_skills))
    
    return {
        "match_score": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_skills_detected": list(resume_skills)
    }