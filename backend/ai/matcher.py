import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class AITalentMatcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan")
            
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-3.6-flash"

    def match(self, candidate_data: dict, job_data: dict) -> dict:
        """
        Mencocokkan kandidat dengan pekerjaan menggunakan AI
        
        Args:
            candidate_data: Dict dari TalentAnalyzer
            job_data: Dict dari JobAnalyzer
        
        Returns:
            Dict dengan match_score, matched_skills, missing_skills, reason, recommendation
        """
        
        # Format skills untuk prompt
        candidate_skills = ", ".join(candidate_data.get("skills", []))
        candidate_exp = candidate_data.get("experience", [])
        
        # Format experience
        exp_text = ""
        if candidate_exp:
            for exp in candidate_exp:
                exp_text += f"- {exp.get('position', '')} di {exp.get('company', '')} ({exp.get('duration_months', 0)} bulan)\n"
        else:
            exp_text = "Tidak ada pengalaman"
        
        # Format job skills
        job_skills = ", ".join(job_data.get("requirements", {}).get("skills", []))
        
        prompt = f"""
You are an AI Recruiter for AI-UNER, an AI-powered recruitment platform.

TASK: Match the following candidate with the job requirement and provide a detailed analysis.

=== CANDIDATE PROFILE ===
Name: {candidate_data.get('name', 'Unknown')}
Skills: {candidate_skills}
Experience:
{exp_text}
Education: {candidate_data.get('education', {}).get('level', 'Tidak ada')} - {candidate_data.get('education', {}).get('major', '')}
Location: {candidate_data.get('location', 'Unknown')}
Desired Positions: {', '.join(candidate_data.get('desired_positions', []))}

=== JOB REQUIREMENT ===
Job Title: {job_data.get('job_title', 'Unknown')}
Required Skills: {job_skills}
Description: {job_data.get('job_description', '')}
Required Experience: {job_data.get('requirements', {}).get('experience_months', 0)} bulan
Education Level: {job_data.get('requirements', {}).get('education_level', 'Not specified')}
Location: {job_data.get('location', 'Unknown')}
Work Type: {job_data.get('work_preferences', {}).get('work_location_type', 'Not specified')}

=== ANALYSIS REQUIRED ===
Analyze the following aspects:
1. **Skill Match**: Compare candidate's skills with job requirements
2. **Experience Match**: Check if candidate's experience matches requirements
3. **Education Match**: Check if education level matches
4. **Location Match**: Check location compatibility
5. **Overall Fit**: Overall assessment

=== OUTPUT FORMAT ===
Return ONLY valid JSON with this structure:
{{
    "match_score": 87,
    "matched_skills": ["HTML", "CSS", "JavaScript"],
    "missing_skills": ["React"],
    "reason": "Candidate has 3 out of 4 required skills. Experience in web development is relevant. However, React is missing.",
    "recommendation": "Consider learning React or applying for a junior position that doesn't require React.",
    "skill_match_details": "3/4 skills match",
    "experience_match": "Relevant experience",
    "education_match": "Match",
    "location_match": "Candidate location matches"
}}

Return ONLY valid JSON. Do NOT use Markdown, code blocks, or any other formatting.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            raw_response = response.text.strip()
            
            # Clean response
            if raw_response.startswith("```json"):
                raw_response = raw_response.replace("```json", "").replace("```", "").strip()
            elif raw_response.startswith("```"):
                raw_response = raw_response.replace("```", "").strip()
            
            result = json.loads(raw_response)
            
            # Validasi minimal
            required_keys = ["match_score", "matched_skills", "missing_skills", "reason"]
            for key in required_keys:
                if key not in result:
                    result[key] = None if key != "match_score" else 50
            
            return result
            
        except json.JSONDecodeError as e:
            return {
                "match_score": 50,
                "matched_skills": [],
                "missing_skills": [],
                "reason": f"Error parsing AI response: {str(e)}",
                "recommendation": "Silakan coba lagi",
                "skill_match_details": "Error",
                "experience_match": "Error",
                "education_match": "Error",
                "location_match": "Error"
            }
        except Exception as e:
            return {
                "match_score": 50,
                "matched_skills": [],
                "missing_skills": [],
                "reason": f"Error: {str(e)}",
                "recommendation": "Silakan coba lagi",
                "skill_match_details": "Error",
                "experience_match": "Error",
                "education_match": "Error",
                "location_match": "Error"
            }