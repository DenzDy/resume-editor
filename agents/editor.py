import os
import re
from llm_client import get_llm_client, get_default_model

class EditorAgent:
    def __init__(self):
        self.client = get_llm_client()
        self.model = get_default_model()
        
    def edit_job_block(self, job_block: str, jd_requirements: str, interactive=True) -> str:
        sys_prompt = (
            "You are a highly strict Resume Copyeditor. You will receive a SINGLE job block in Typst code, and a list of JOB REQUIREMENTS.\n"
            "Your task is to rephrase the EXISTING bullet points (`- `) to highlight any skills that naturally match the JOB REQUIREMENTS.\n\n"
            "CRITICAL ANTI-HALLUCINATION RULES:\n"
            "1. DO NOT ADD NEW TECHNOLOGIES OR SKILLS. You may only emphasize what is already in the original text. Do not invent experience like 'GraphQL' or 'AWS' if it wasn't mentioned.\n"
            "2. STOPPER RULE: If an original bullet point has absolutely no relevance to the job requirements, DO NOT EDIT IT. Leave it exactly as it is.\n"
            "3. DO NOT create fake companies or jobs. ONLY edit existing bullet points.\n"
            "4. PRESERVE the exact Typst formatting: `#company-heading(...)` and `#job-heading(...)` must remain untouched.\n"
            "5. You MUST wrap your final Typst code inside `<updated_job>` and `</updated_job>` tags. Do not output conversational text.\n\n"
            "EXAMPLE TYPST OUTPUT:\n"
            "<updated_job>\n"
            '#company-heading("Acme Corp", start: "2023")[ \n'
            '  #job-heading("Intern")[ \n'
            '    - Developed backend automation scripts. \n'
            '  ]\n'
            ']\n'
            "</updated_job>\n"
        )
        
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"JOB REQUIREMENTS:\n{jd_requirements}\n\nCURRENT JOB BLOCK:\n{job_block}"}
        ]
        
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            content = response.choices[0].message.content
            
            if interactive and content.strip().startswith("QUESTION:"):
                question = content.replace("QUESTION:", "").strip()
                print(f"\n[Editor Agent asks]: {question}")
                user_answer = input("Your answer: ")
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": user_answer})
            else:
                match = re.search(r'<updated_job>(.*?)</updated_job>', content, re.DOTALL | re.IGNORECASE)
                if match:
                    return match.group(1).strip()
                else:
                    return content.replace("```typst", "").replace("```", "").strip()
