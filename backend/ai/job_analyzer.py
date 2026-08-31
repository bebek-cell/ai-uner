import json
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Ambil API Key langsung dari environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class JobAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan")
            
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-3.6-flash"  # Model terbaru

    def analyze(self, job_text: str) -> dict:
        prompt = f"""
You are the Job Profile Analyzer for AI-UNER, an AI-powered recruitment platform.

TASK: Extract structured information from the following job vacancy text.

JOB VACANCY:
{job_text}

IMPORTANT RULES:
1. Extract ONLY information that is clearly stated in the job vacancy
2. DO NOT invent or assume any information
3. Use null for missing information
4. Skills must be a list of strings
5. Responsibilities must be a list of strings
6. experience_months must be a number or null
7. Salary values must be numbers or null
8. All arrays must be valid JSON arrays

OUTPUT FORMAT (JSON only, no other text):
{{
    "job_title": "string or null",
    "employer": "string or null",
    "location": "string or null",
    "employment_type": "string or null",
    "salary_range": {{
        "min": number or null,
        "max": number or null,
        "currency": "string or null"
    }},
    "requirements": {{
        "education_level": "string or null",
        "skills": ["skill1", "skill2"],
        "experience_months": number or null
    }},
    "responsibilities": ["task1", "task2"],
    "work_preferences": {{
        "work_location_type": "string or null",
        "working_hours": "string or null"
    }}
}}

Return ONLY valid JSON. Do NOT use Markdown, code blocks, or any other formatting.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            raw_response = response.text.strip()
            
            # Clean response dari kemungkinan markdown
            if raw_response.startswith("```json"):
                raw_response = raw_response.replace("```json", "").replace("```", "").strip()
            elif raw_response.startswith("```"):
                raw_response = raw_response.replace("```", "").strip()
            
            job_profile = json.loads(raw_response)
            return job_profile

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Gemini returned invalid JSON for job analysis:\n\n{raw_response[:500]}..."
            ) from error
        except Exception as error:
            raise ValueError(f"Error calling Gemini API: {str(error)}")