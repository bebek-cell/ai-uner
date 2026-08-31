import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # AI Model - Pake yang terbaru
    AI_MODEL = "gemini-3.6-flash"  # <-- Update ini
    
    # Server
    HOST = "0.0.0.0"
    PORT = 8000
    
    # CORS
    ALLOWED_ORIGINS = ["*"]
    
    # File Upload
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

if not Config.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di .env")