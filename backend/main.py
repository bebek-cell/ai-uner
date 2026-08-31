from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Hapus 'backend.' dari import
from ai.talent_analyzer import TalentAnalyzer  # <-- Hapus backend.
from ai.job_analyzer import JobAnalyzer        # <-- Hapus backend.
from ai.matcher import AITalentMatcher         # <-- Hapus backend.

load_dotenv()

app = FastAPI(
    title="AI-UNER API",
    description="AI-Powered Recruitment Matching Platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== SCHEMAS ====

class CandidateProfile(BaseModel):
    name: Optional[str] = None
    skills: List[str] = []
    experience: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    desired_positions: List[str] = []

class JobRequirement(BaseModel):
    job_title: str
    job_skills: List[str] = []
    job_description: Optional[str] = None
    required_experience: Optional[int] = None
    education_level: Optional[str] = None
    location: Optional[str] = None

class MatchRequest(BaseModel):
    candidate: CandidateProfile
    job: JobRequirement

class MatchResponse(BaseModel):
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    reason: str
    recommendation: Optional[str] = None
    skill_match_details: Optional[str] = None
    experience_match: Optional[str] = None
    education_match: Optional[str] = None
    location_match: Optional[str] = None

class AnalyzeCVRequest(BaseModel):
    cv_text: str

class AnalyzeJobRequest(BaseModel):
    job_text: str

# ==== ENDPOINTS ====

@app.get("/")
def root():
    return {
        "message": "AI-UNER API is running",
        "version": "1.0.0",
        "endpoints": {
            "/api/match": "POST - Match candidate to job",
            "/api/analyze-cv": "POST - Analyze CV text",
            "/api/analyze-job": "POST - Analyze job description",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "gemini-3.6-flash"}

@app.post("/api/analyze-cv")
async def analyze_cv(request: AnalyzeCVRequest):
    """Analyze CV text and extract structured information"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found")
        
        analyzer = TalentAnalyzer(api_key)
        profile = analyzer.analyze(request.cv_text)
        return profile
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-job")
async def analyze_job(request: AnalyzeJobRequest):
    """Analyze job description and extract structured information"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found")
        
        analyzer = JobAnalyzer(api_key)
        job_profile = analyzer.analyze(request.job_text)
        return job_profile
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/match", response_model=MatchResponse)
async def match_candidate_to_job(request: MatchRequest):
    """Match a candidate to a job using AI"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found")
        
        # Convert to dict
        candidate_data = request.candidate.dict()
        job_data = request.job.dict()
        
        # Run matching
        matcher = AITalentMatcher(api_key)
        result = matcher.match(candidate_data, job_data)
        
        return MatchResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/match-batch")
async def match_candidate_to_jobs(candidate: CandidateProfile, jobs: List[JobRequirement]):
    """Match a candidate to multiple jobs"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="GEMINI_API_KEY not found")
        
        matcher = AITalentMatcher(api_key)
        results = []
        
        for job in jobs:
            result = matcher.match(candidate.dict(), job.dict())
            results.append(result)
        
        # Sort by match_score descending
        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        return {"matches": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # <-- Ganti dari "backend.main:app" jadi "main:app"
        host="0.0.0.0",
        port=8000,
        reload=True
    )