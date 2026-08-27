import json
from google import genai


class JobAnalyzer:

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def analyze(self, job_text: str) -> dict:

        prompt = f"""
You are the Job Profile Analyzer for HeadHunter,
an AI-powered platform connecting job seekers with employers.

Your task is to extract structured information from a job vacancy.

JOB VACANCY:
{job_text}

Return ONLY valid JSON using exactly this structure:

{{
    "job_title": null,
    "employer": null,
    "location": null,
    "employment_type": null,
    "salary_range": {{
        "min": null,
        "max": null,
        "currency": null
    }},
    "requirements": {{
        "education_level": null,
        "skills": [],
        "experience_months": null
    }},
    "responsibilities": [],
    "work_preferences": {{
        "work_location_type": null,
        "working_hours": null
    }}
}}

RULES:

1. Extract only information explicitly available in the job vacancy.
2. Never invent or assume information.
3. Use null when information is unavailable.
4. skills must be an array of strings.
5. responsibilities must be an array of strings.
6. experience_months must be a number or null.
7. salary values must be numbers or null.
8. Preserve the meaning of the original vacancy.
9. Return ONLY JSON.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_response = response.text.strip()

        try:
            job_profile = json.loads(raw_response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "Gemini menghasilkan JSON lowongan yang tidak valid.\n\n"
                f"Response:\n{raw_response}"
            ) from error

        return job_profile