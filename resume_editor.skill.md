# Resume Editor Skill

This skill provides instructions for the agent to autonomously edit a Typst resume against a job description.

## Instructions
1. When the user asks to edit their resume, ask them for the path to their `.typ` file and the Job Description URL (or text).
2. Read the Typst file contents.
3. If they provide a URL, fetch it using Playwright (via the local Python script `utils/web_scraper.py` or directly if you have access).
4. Parse the experience section from the Typst code.
5. Use your reasoning capabilities to refine the experience section to better match the job description, WITHOUT falsifying information.
6. If information is missing, pause and ask the user for clarification.
7. Present the updated Typst code to the user and calculate a Match Score (0-100) detailing how well the updated resume fits the job description.
