import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.editor import EditorAgent
from agents.screener import ScreenerAgent
from utils.typst_parser import extract_experience, replace_experience, extract_job_blocks, replace_job_block
from utils.web_scraper import scrape_job_description_sync

def main():
    print("--- Multi-Agent Resume Editor ---")
    typst_path = input("Enter path to Typst resume file (.typ): ")
    if not os.path.exists(typst_path):
        print("File not found.")
        return
        
    with open(typst_path, 'r', encoding='utf-8') as f:
        typst_code = f.read()
        
    jd_input = input("Enter Job Description URL (or paste text directly): ")
    if jd_input.startswith("http"):
        print("Scraping job description...")
        jd_text = scrape_job_description_sync(jd_input)
    else:
        jd_text = jd_input
        
    screener = ScreenerAgent()
    print("\n[Screener Agent] Extracting core job requirements...")
    jd_reqs = screener.extract_jd_requirements(jd_text)
    print("--- Core Requirements ---\n" + jd_reqs + "\n-------------------------")
        
    print("\n[Orchestrator] Extracting experience section...")
    current_experience = extract_experience(typst_code)
    if not current_experience:
        print("Could not locate Experience section in Typst code.")
        return
        
    jobs = extract_job_blocks(current_experience)
    if not jobs:
        print("Could not locate any #company-heading blocks.")
        return
        
    print(f"\n[Orchestrator] Handing off to Editor Agent to process {len(jobs)} jobs...")
    editor = EditorAgent()
    updated_experience = current_experience
    
    for i, job in enumerate(jobs):
        print(f"-> Editing Job {i+1} of {len(jobs)}...")
        updated_job = editor.edit_job_block(job, jd_reqs, interactive=True)
        updated_experience = replace_job_block(updated_experience, job, updated_job)
    
    print("\n[Orchestrator] Rebuilding resume...")
    updated_typst = replace_experience(typst_code, current_experience, updated_experience)
    out_path = typst_path.replace(".typ", "_updated.typ")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(updated_typst)
    print(f"Updated resume saved to {out_path}")
    
    print("\n[Orchestrator] Handing off to Screener Agent...")
    result = screener.score_resume(updated_typst, jd_reqs)
    print(f"\n--- MATCH SCORE: {result['score']} ---")
    print(result['justification'])

if __name__ == "__main__":
    main()
