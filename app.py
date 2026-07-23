import streamlit as st
import sys
import os

# Ensure utils and agents are in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.editor import EditorAgent
from agents.screener import ScreenerAgent
from utils.typst_parser import extract_experience, replace_experience, extract_job_blocks, replace_job_block
from utils.web_scraper import scrape_job_description_sync

st.set_page_config(page_title="Multi-Agent Resume Editor", layout="wide")
st.title("Multi-Agent Resume Editor")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Typst Code")
    typst_code = st.text_area("Paste your Typst resume code here:", height=300)
    
with col2:
    st.subheader("Job Description")
    jd_url = st.text_input("Job Description URL (optional):")
    jd_text = st.text_area("Or paste Job Description text:", height=200)

if st.button("Analyze & Edit"):
    if not typst_code:
        st.error("Please provide Typst code.")
        st.stop()
        
    if jd_url:
        with st.spinner("Scraping job description..."):
            jd_content = scrape_job_description_sync(jd_url)
    else:
        jd_content = jd_text
        
    screener = ScreenerAgent()
    with st.spinner("Extracting Core Requirements from Job Description..."):
        jd_requirements = screener.extract_jd_requirements(jd_content)
        st.info("Extracted Core Requirements:\n" + jd_requirements)

    st.info("Extracting Experience Blocks...")
    current_exp = extract_experience(typst_code)
    
    if not current_exp:
        st.error("Could not extract experience section. Check your Typst syntax.")
        st.stop()
        
    jobs = extract_job_blocks(current_exp)
    if not jobs:
        st.error("Could not find individual #company-heading blocks.")
        st.stop()
        
    editor = EditorAgent()
    updated_exp = current_exp
    
    progress_text = "Editor Agent is rewriting your experience block by block..."
    my_bar = st.progress(0, text=progress_text)
    
    for i, job in enumerate(jobs):
        updated_job = editor.edit_job_block(job, jd_requirements, interactive=False)
        updated_exp = replace_job_block(updated_exp, job, updated_job)
        my_bar.progress((i + 1) / len(jobs), text=f"Edited Job {i+1} of {len(jobs)}")
        
    st.success("Experience Updated!")
    
    updated_typst = replace_experience(typst_code, current_exp, updated_exp)
    st.subheader("Updated Typst Code")
    st.code(updated_typst, language="typst")
    
    with st.spinner("Screener Agent is scoring..."):
        result = screener.score_resume(updated_typst, jd_requirements)
    
    st.metric(label="Match Score", value=result["score"])
    st.write(result["justification"])
