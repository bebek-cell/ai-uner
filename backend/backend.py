import os
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ai JobHunt API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class MatchRequest(BaseModel):
    job_description: str
    candidate_resume: str

@app.post("/api/match")
def calculate_match(data: MatchRequest):
    corpus = [data.job_description, data.candidate_resume]


    vectorizer =
