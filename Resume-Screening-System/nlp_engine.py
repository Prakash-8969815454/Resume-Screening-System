import re
from typing import List, Dict, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Standard skills taxonomy dictionary
COMMON_SKILLS = {
    # 0. Technical & Professional Skills (Industry-Specific)

    "python", "java", "c++", "javascript", "typescript", "html", "css", "react", 
    "angular", "vue", "node.js", "fastapi", "django", "flask", "sql", "postgresql", 
    "mysql", "mongodb", "docker", "kubernetes", "aws", "azure", "git", "github", 
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch", "pandas", 
    "numpy", "scikit-learn", "rest api", "graphql", "agile", "devops", "ci/cd","aiml",
    "statistics", "probability","matplotlib", "kafka", "pyspark", "hadoop", "spark",
    "etl","elt","pipelne","cloud", "vscode", "jupiternotebook", "databricks", "logical reasoning",
    "php","c", "ruby", "swift", "objective-c", "r", "sas", "stata", "matlab", "excel",
    "oops","opearting system","computer fundamentals",
    
    # 1. Foundational & Basic Literacy Skills (Universal)
    "Reading Comprehension",
    "Writing","Documentation",
    "Basic","Applied Mathematics",
    "Active Listening",
    "Verbal Communication","Speaking",
    
    # 2. Cognitive & Thinking Skills (Knowledge Work & Analytical Roles)
    "Critical Thinking",
    "Complex Problem Solving",
    "Deductive and Inductive Reasoning",
    "Judgment and Decision Making",
    "Active Learning and Continuous Adaptability",
    "Information Ordering and Pattern Recognition",
    "Systems Analysis and Evaluation",

    # 3. Interpersonal, Social & Customer Service Skills (Universal)
    "Team Coordination", "Collaboration",
    "Customer Service", "Client Relations",
    "Negotiation", "Conflict Resolution",
    "Persuasion", "Influencing",
    "Social Perceptiveness", "Empathy",
    "Instruction", "Training", "Mentoring",

    # 4. Self-Management & Work Ethic (All Sectors)
    "Time Management", "Punctuality",
    "Adaptability", "Workplace Agility",
    "Stress Tolerance", "Resilience",
    "Reliability", "Accountability", "Work Ethic",
    "Attention to Detail", "Quality Control",

    # 5. Digital & Technical Skills (Modern Offices & Tech Roles)
    "Digital Literacy","Navigation",
    "Data Literacy","Spreadsheet Proficiency", "Excel","Google Sheets",
    "Collaboration", "Software Usage Slack", "Teams", "Zoom",
    "Generative AI", "Productivity", "Tool Utilization",
    "Software Development","Programming" ,
    "IT Support", "Hardware Setup", "Network" "Troubleshooting",
    "Cybersecurity" ,"Fundamentals",

    # 6. Vocational, Manual & Physical Skills (Trades, Manufacturing, Construction, Agriculture)
    "Manual Dexterity"," Control Precision",
    "Multilimb Coordination", "Spatial Awareness",
    "Mechanical Comprehension","Equipment Repair",
    "Heavy Machinery","Vehicle Operation",
    "Physical Stamina", "Strength",  "Endurance",
    "Precision Tool", "Handling","Assembly",
    "Carpentry", "Plumbing", "Electrical", "Welding",
    "Agricultural", "Harvesting",  "Fieldwork Techniques",

    # 7. Management & Resource Operations (Leadership & Logistics)
    "Project Management","Workflow Planning",
    "Personnel","Human Resource Management",
    "Financial Literacy","Budgeting",
    "Material", "Stock",  "Inventory Resource Management",
    "Administrative","Office Organization"
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