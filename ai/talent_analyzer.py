import json
from google import genai


class TalentAnalyzer:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def analyze(self, cv_text: str) -> dict:

        prompt = f"""
You are the Talent Profile Analyzer for HeadHunter,
an AI-powered platform connecting job seekers with employers.

Your task is to extract structured information from a candidate's CV.

CANDIDATE CV:
{cv_text}

Return ONLY valid JSON using exactly this structure:

{{
    "name": null,
    "education": {{
        "level": null,
        "institution": null,
        "major": null
    }},
    "location": null,
    "skills": [],
    "experience": [
        {{
            "position": null,
            "company": null,
            "duration_months": null,
            "responsibilities": []
        }}
    ],
    "desired_positions": [],
    "work_preferences": {{
        "employment_type": null,
        "preferred_location": null,
        "salary_expectation": null
    }}
}}

RULES:

1. Extract only information explicitly available in the CV.
2. Never invent or assume information.
3. Use null when information is unavailable.
4. skills must be an array of strings.
5. experience must be an array.
6. duration_months must be a number or null.
7. desired_positions must be an array of strings.
8. responsibilities must be an array of strings.
9. Preserve the meaning of the original CV.
10. Return ONLY JSON. Do not use Markdown fences.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        raw_response = response.text.strip()

        try:
            profile = json.loads(raw_response)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Gemini returned invalid JSON:\n{raw_response}"
            ) from error

        return profile