import re

def extract_experience(typst_code: str) -> str:
    """Extracts the experience section from typst markup, looking specifically for the = Experience header."""
    # Capture everything from = Experience up to the next line that starts with = 
    match = re.search(r'(^={1,6}\s*Experience\b.*?)(?=\n={1,6}\s+)', typst_code, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1).strip()
    
    # Fallback: if Experience is the last section
    match_end = re.search(r'(^={1,6}\s*Experience\b.*)', typst_code, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if match_end:
        return match_end.group(1).strip()
    return ""

def extract_job_blocks(experience_section: str) -> list:
    """
    Extracts individual job entries marked by #company-heading and #job-heading.
    Returns a list of strings, each containing one complete company/job block.
    """
    # Split the section by #company-heading to isolate individual jobs
    blocks = re.split(r'(?=#company-heading\()', experience_section)
    jobs = []
    for block in blocks:
        if '#company-heading' in block and '#job-heading' in block:
            jobs.append(block.strip())
    return jobs

def replace_experience(original_typst: str, old_experience: str, new_experience: str) -> str:
    """Safely replace the exact chunk of experience text in the original document."""
    if old_experience and old_experience in original_typst:
        return original_typst.replace(old_experience, new_experience)
    return original_typst

def replace_job_block(original_typst: str, old_job_block: str, new_job_block: str) -> str:
    """Replaces a specific #company-heading block in the typst code."""
    if old_job_block and old_job_block in original_typst:
        return original_typst.replace(old_job_block, new_job_block)
    return original_typst
