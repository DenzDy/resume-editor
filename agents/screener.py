import os
from llm_client import get_llm_client, get_default_model

class ScreenerAgent:
    def __init__(self):
        self.client = get_llm_client()
        self.model = get_default_model()
        
    def extract_jd_requirements(self, raw_jd: str) -> str:
        sys_prompt = (
            "You are an expert Technical Recruiter. Extract the core required skills, technologies, and responsibilities from the following Job Description. "
            "Output ONLY a concise bulleted list of the absolute core requirements. Ignore company background, benefits, and fluff."
        )
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"JOB DESCRIPTION:\n{raw_jd}"}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
        
    def score_resume(self, updated_resume: str, jd_requirements: str) -> dict:
        sys_prompt = (
            "You are a strict HR Verifier and Screener. Compare the updated resume against the core Job Requirements. "
            "Output a Match Score from 0-100 on the first line exactly formatted as 'SCORE: 85', followed by a brief justification."
        )
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"JOB REQUIREMENTS:\n{jd_requirements}\n\nUPDATED RESUME:\n{updated_resume}"}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0
        )
        content = response.choices[0].message.content
        
        score = 0
        justification = content
        for line in content.split('\n'):
            if line.startswith('SCORE:'):
                try:
                    score = int(line.replace('SCORE:', '').strip())
                except:
                    pass
                break
                
        return {"score": score, "justification": justification}
