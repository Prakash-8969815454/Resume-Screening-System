import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'ats_screener.db')}"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)