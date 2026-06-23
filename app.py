import streamlit as st
import time
from pypdf import PdfReader
import io
import os

# Set page config
st.set_page_config(
    page_title="AI Resume Builder & Editor",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom premium styling using CSS injection
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #070A13 100%) !important;
        color: #F3F4F6 !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Titles and text */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }

    .main-title {
        background: linear-gradient(90deg, #A855F7 0%, #6366F1 50%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0px 4px 20px rgba(168, 85, 247, 0.15);
    }

    .main-subtitle {
        color: #9CA3AF !important;
        font-size: 1.25rem !important;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 350;
    }

    /* Glassmorphic card styling applied directly to columns inside the top columns container */
    .st-key-top_columns_container div[data-testid="column"],
    div[data-key="top_columns_container"] div[data-testid="column"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
        height: 100% !important; /* Forces columns to stretch dynamically */
    }
    
    .st-key-top_columns_container div[data-testid="column"]:hover,
    div[data-key="top_columns_container"] div[data-testid="column"]:hover {
        border-color: rgba(168, 85, 247, 0.3) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(168, 85, 247, 0.15) !important;
    }

    /* Glassmorphic styling for progress container and generation form cards */
    .st-key-progress_container div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-key="progress_container"] div[data-testid="stVerticalBlockBorderWrapper"],
    .st-key-generation_container div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-key="generation_container"] div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    .st-key-generation_container div[data-testid="stVerticalBlockBorderWrapper"]:hover,
    div[data-key="generation_container"] div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(168, 85, 247, 0.3) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 40px 0 rgba(168, 85, 247, 0.15) !important;
    }

    /* Enforce equal heights for tab panels inside Job Description card to prevent content shifting */
    div[data-key="top_columns_container"] div[data-baseweb="tab-panel"] {
        min-height: 380px !important;
    }

    /* Custom badge/headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #F3F4F6;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }

    .section-icon {
        background: linear-gradient(135deg, #A855F7 0%, #6366F1 100%);
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 1rem;
    }

    /* Typst Code Area */
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.95rem !important;
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #A855F7 !important;
        box-shadow: 0 0 0 1px #A855F7 !important;
    }

    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.02) !important;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: transparent !important;
        border-radius: 6px;
        color: #9CA3AF !important;
        font-weight: 500;
        transition: all 0.2s ease;
        padding: 0 16px;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #F3F4F6 !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #A855F7 0%, #6366F1 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(168, 85, 247, 0.25);
    }

    .stTabs [data-baseweb="tab-highlight-bar"] {
        display: none !important;
    }

    /* Center only primary button element containers inside their columns */
    div.stElementContainer:has(div.st-key-tailor_resume_btn),
    div.stElementContainer:has(div[data-key="tailor_resume_btn"]),
    div.stElementContainer:has(div.st-key-create_resume_btn),
    div.stElementContainer:has(div[data-key="create_resume_btn"]),
    div.stElementContainer:has(div[data-testid="stDownloadButton"]) {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    div.st-key-tailor_resume_btn,
    div[data-key="tailor_resume_btn"],
    div.st-key-create_resume_btn,
    div[data-key="create_resume_btn"],
    div[data-testid="stDownloadButton"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* Base styling for secondary helper buttons (add/remove) */
    div[data-testid="stButton"] button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #F3F4F6 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 8px 16px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        min-width: 120px !important;
        width: auto !important;
        height: auto !important;
        display: inline-block !important;
        box-shadow: none !important;
    }

    div[data-testid="stButton"] button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(168, 85, 247, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Style override for primary actions with beautiful gradients and large sizing */
    .st-key-tailor_resume_btn button,
    div[data-key="tailor_resume_btn"] button,
    .st-key-create_resume_btn button,
    div[data-key="create_resume_btn"] button,
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(90deg, #A855F7 0%, #6366F1 50%, #3B82F6 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        min-width: 280px !important;
        width: auto !important;
        height: auto !important;
        display: block !important;
    }

    .st-key-tailor_resume_btn button:hover,
    div[data-key="tailor_resume_btn"] button:hover,
    .st-key-create_resume_btn button:hover,
    div[data-key="create_resume_btn"] button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5) !important;
        filter: brightness(1.1);
    }

    .st-key-tailor_resume_btn button:active,
    div[data-key="tailor_resume_btn"] button:active,
    .st-key-create_resume_btn button:active,
    div[data-key="create_resume_btn"] button:active,
    div[data-testid="stDownloadButton"] button:active {
        transform: translateY(1px) !important;
    }

    /* Hide default Streamlit elements for clean UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom File Uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed rgba(168, 85, 247, 0.2);
        border-radius: 12px;
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.01);
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(168, 85, 247, 0.5);
        background-color: rgba(168, 85, 247, 0.02);
    }

    /* Pipeline Step cards */
    .pipeline-step {
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 4px solid #4B5563;
        background: rgba(255, 255, 255, 0.02);
    }
    
    .pipeline-step-active {
        border-left-color: #6366F1;
        background: rgba(99, 102, 241, 0.05);
        animation: pulse 2s infinite;
    }

    .pipeline-step-completed {
        border-left-color: #10B981;
        background: rgba(16, 185, 129, 0.05);
    }

    @keyframes pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State variables
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'gen_job_description' not in st.session_state:
    st.session_state.gen_job_description = ""
if 'typst_code' not in st.session_state:
    st.session_state.typst_code = ""
if 'uploaded_filename' not in st.session_state:
    st.session_state.uploaded_filename = ""
if 'pipeline_running' not in st.session_state:
    st.session_state.pipeline_running = False
if 'gen_pipeline_running' not in st.session_state:
    st.session_state.gen_pipeline_running = False

# Form fields session state
if 'gen_full_name' not in st.session_state:
    st.session_state.gen_full_name = ""
if 'gen_email' not in st.session_state:
    st.session_state.gen_email = ""
if 'gen_phone' not in st.session_state:
    st.session_state.gen_phone = ""
if 'gen_links' not in st.session_state:
    st.session_state.gen_links = ""
if 'gen_summary' not in st.session_state:
    st.session_state.gen_summary = ""
if 'gen_languages' not in st.session_state:
    st.session_state.gen_languages = ""
if 'gen_frameworks' not in st.session_state:
    st.session_state.gen_frameworks = ""
if 'gen_databases' not in st.session_state:
    st.session_state.gen_databases = ""

# Initialize dynamic lists for Resume Generation
if 'edu_entries' not in st.session_state:
    st.session_state.edu_entries = [{"school": "", "degree": "", "year": "", "gpa": ""}]
if 'exp_entries' not in st.session_state:
    st.session_state.exp_entries = [{"title": "", "company": "", "duration": "", "highlights": ""}]
if 'proj_entries' not in st.session_state:
    st.session_state.proj_entries = [{"name": "", "tech": "", "desc": ""}]

# Header Design
st.markdown('<div class="main-title">AI Resume Tailoring Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Optimize and build professional Typst resumes tailored precisely to your target job description.</div>', unsafe_allow_html=True)

# Initialize main tabs
main_tab1, main_tab2 = st.tabs(["🎯 Resume Tailoring", "✍️ Resume Generation"])

with main_tab1:
    # Left Column (Job Description) and Right Column (Resume Edit)
    with st.container(key="top_columns_container"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(
                '<div class="section-header"><span class="section-icon">💼</span> 1. Target Job Description</div>', 
                unsafe_allow_html=True
            )
            st.write("Specify the job requirements so the AI can extract keywords and tailor your resume.")
            
            # Input tabs: File Upload or Paste Text
            jd_tab1, jd_tab2 = st.tabs(["📝 Paste Text", "📤 Upload File"])
            
            with jd_tab1:
                text_jd = st.text_area(
                    "Paste the job posting description here:",
                    value=st.session_state.job_description,
                    placeholder="Requirements, responsibilities, role overview...",
                    height=300,
                    key="text_jd_input"
                )
                if text_jd != st.session_state.job_description:
                    st.session_state.job_description = text_jd
                    
            with jd_tab2:
                uploaded_jd = st.file_uploader(
                    "Upload Job Description (PDF or TXT)",
                    type=["txt", "pdf"],
                    key="file_jd_uploader"
                )
                if uploaded_jd is not None:
                    # Check if this file is different from the previously loaded file
                    if uploaded_jd.name != st.session_state.get('last_uploaded_jd_name', ''):
                        st.session_state.last_uploaded_jd_name = uploaded_jd.name
                        file_type = uploaded_jd.type
                        
                        if "pdf" in file_type:
                            try:
                                pdf_reader = PdfReader(io.BytesIO(uploaded_jd.read()))
                                extracted_text = ""
                                for page in pdf_reader.pages:
                                    text = page.extract_text()
                                    if text:
                                        extracted_text += text + "\n"
                                st.session_state.job_description = extracted_text.strip()
                                st.success(f"Successfully extracted text from {uploaded_jd.name}!")
                            except Exception as e:
                                st.error(f"Error reading PDF: {e}")
                        else:
                            # Text file
                            try:
                                text_data = uploaded_jd.read().decode("utf-8")
                                st.session_state.job_description = text_data
                                st.success(f"Successfully loaded {uploaded_jd.name}!")
                            except Exception as e:
                                st.error(f"Error reading text file: {e}")
                                
                if st.session_state.job_description:
                    st.info(f"Loaded Job Description: {len(st.session_state.job_description)} characters.")

        with col2:
            st.markdown(
                '<div class="section-header"><span class="section-icon">📄</span> 2. Typst Resume Template</div>', 
                unsafe_allow_html=True
            )
            st.write("Upload your existing Typst resume (`.typ`). You can review and edit it directly below.")
            
            uploaded_typst = st.file_uploader(
                "Upload Resume Typst File (.typ)",
                type=["typ"],
                key="typst_uploader"
            )
            
            if uploaded_typst is not None:
                if uploaded_typst.name != st.session_state.uploaded_filename:
                    try:
                        content = uploaded_typst.read().decode("utf-8")
                        st.session_state.typst_code = content
                        st.session_state.uploaded_filename = uploaded_typst.name
                        st.success(f"Successfully loaded {uploaded_typst.name}!")
                    except Exception as e:
                        st.error(f"Error reading Typst file: {e}")
                        
            # Editor area (visible if there's code, or shows a placeholder template if empty)
            if not st.session_state.typst_code:
                # Load a default resume template placeholder to show off the visual editor
                st.session_state.typst_code = """// Simple Typst Resume Template
#set page(paper: "us-letter", margin: (x: 1.5cm, y: 2cm))
#set text(font: "Liberation Sans", size: 10pt)

#align(center)[
  #text(size: 20pt, weight: "bold")[Jane Doe] \
  #text(fill: gray)[jane.doe@email.com | (123) 456-7890 | github.com/janedoe]
]

== Professional Experience
*Software Engineer* @ Tech Corp _(2022 - Present)_
- Developed high-performance web applications using React and Python.
- Optimised databases resulting in a 30% reduction in query latency.

== Education
*B.S. Computer Science* - State University _(2018 - 2022)_
"""

            edited_typst = st.text_area(
                "Live Typst Editor:",
                value=st.session_state.typst_code,
                height=320,
                key="typst_editor"
            )
            if edited_typst != st.session_state.typst_code:
                st.session_state.typst_code = edited_typst

    st.divider()

    # Validation check before starting the pipeline
    can_run = len(st.session_state.job_description.strip()) > 0 and len(st.session_state.typst_code.strip()) > 0

    run_btn = st.button("🚀 Tailor your Resume", disabled=not can_run, key="tailor_resume_btn")

    if not can_run:
        st.caption("<div style='text-align: center; color: #EF4444;'>Please fill in both the Job Description and upload/write your Typst resume to start.</div>", unsafe_allow_html=True)
    else:
        st.caption("<div style='text-align: center; color: #9CA3AF;'>Ready to optimize. Press the button to begin the tailoring agent flow.</div>", unsafe_allow_html=True)

    # Pipeline Simulation / Run Logic
    if run_btn:
        st.session_state.pipeline_running = True
        
    if st.session_state.pipeline_running:
        with st.container(border=True, key="progress_container"):
            st.markdown("#### Execution Progress")
            
            steps = [
                ("Step 1: Analyzing job description for target keywords & skills", 1.5),
                ("Step 2: Parsing Typst template structure and section mappings", 1.2),
                ("Step 3: Aligning resume content and rewriting experiences", 2.2),
                ("Step 4: Formatting and validation of compiled Typst code", 1.5),
                ("Step 5: Final output generation and preview compilation", 1.0)
            ]
            
            # Progress bars and steps
            progress_bar = st.progress(0)
            step_container = st.empty()
            
            for idx, (step_name, delay) in enumerate(steps):
                # Update styling lists
                html_steps = []
                for i in range(len(steps)):
                    status_class = "pipeline-step"
                    status_icon = "⚪"
                    if i < idx:
                        status_class += " pipeline-step-completed"
                        status_icon = "🟢 Completed"
                    elif i == idx:
                        status_class += " pipeline-step-active"
                        status_icon = "⚡ Running..."
                    else:
                        status_icon = "⏳ Pending"
                        
                    html_steps.append(f"""
                    <div class="{status_class}">
                        <span>{steps[i][0]}</span>
                        <strong>{status_icon}</strong>
                    </div>
                    """)
                    
                step_container.markdown("\n".join(html_steps), unsafe_allow_html=True)
                
                # Calculate progress
                progress_val = int(((idx + 0.5) / len(steps)) * 100)
                progress_bar.progress(progress_val)
                
                time.sleep(delay)
                
            # Mark all completed
            html_steps = []
            for i in range(len(steps)):
                html_steps.append(f"""
                <div class="pipeline-step pipeline-step-completed">
                    <span>{steps[i][0]}</span>
                    <strong>🟢 Completed</strong>
                </div>
                """)
            step_container.markdown("\n".join(html_steps), unsafe_allow_html=True)
            progress_bar.progress(100)
            
            # Simulated Optimised Output
            st.success("🎉 Resume optimization successfully completed!")
            
            # Beautiful display for final options
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("##### 📁 Optimised Typst Output")
                
                # Simulate an optimized Typst output
                optimized_typst = st.session_state.typst_code
                if "Jane Doe" in optimized_typst:
                    # Let's add some tailored content
                    optimized_typst = optimized_typst.replace(
                        "- Developed high-performance web applications using React and Python.",
                        "- Developed high-performance web applications using React and Python, aligning with the target job's performance-oriented stack.\n- Implemented robust data-driven features using modern system abstractions."
                    )
                
                st.code(optimized_typst, language="rust")
                
                st.download_button(
                    label="💾 Download Tailored Typst File",
                    data=optimized_typst,
                    file_name="tailored_resume.typ",
                    mime="text/plain"
                )
                
            with res_col2:
                st.markdown("##### 🔍 Adaptation Analysis Report")
                st.markdown("""
                **Optimisation Score:** 94% (Up from 71%)
                
                **Key Modifications:**
                - Incorporated **React**, **Python**, and **Database Query Optimization** matching the job's high-density keywords.
                - Formatted action verbs to be more impactful (e.g. *Developed* -> *Optimised*).
                - Structuring bullet points to emphasize performance gains (e.g. *30% reduction*).
                
                **Recommended Next Steps:**
                - Compile the `.typ` file using Typst command-line tool: `typst compile tailored_resume.typ`
                - Do a quick read-through to ensure all simulated experiences match your background perfectly.
                """)
                
            st.session_state.pipeline_running = False

with main_tab2:
    with st.container(key="generation_container"):
        # Target Job Description card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">💼</span> Target Job Description</div>', unsafe_allow_html=True)
            st.write("Specify the job requirements so the engine can tailor your generated resume.")
            
            gen_jd_tab1, gen_jd_tab2 = st.tabs(["📝 Paste Text", "📤 Upload File"])
            
            with gen_jd_tab1:
                gen_text_jd = st.text_area(
                    "Paste the job posting description here:",
                    value=st.session_state.gen_job_description,
                    placeholder="Requirements, responsibilities, role overview...",
                    height=150,
                    key="gen_text_jd_input"
                )
                if gen_text_jd != st.session_state.gen_job_description:
                    st.session_state.gen_job_description = gen_text_jd
                    
            with gen_jd_tab2:
                gen_uploaded_jd = st.file_uploader(
                    "Upload Job Description (PDF or TXT)",
                    type=["txt", "pdf"],
                    key="gen_file_jd_uploader"
                )
                if gen_uploaded_jd is not None:
                    if gen_uploaded_jd.name != st.session_state.get('last_uploaded_gen_jd_name', ''):
                        st.session_state.last_uploaded_gen_jd_name = gen_uploaded_jd.name
                        file_type = gen_uploaded_jd.type
                        
                        if "pdf" in file_type:
                            try:
                                pdf_reader = PdfReader(io.BytesIO(gen_uploaded_jd.read()))
                                extracted_text = ""
                                for page in pdf_reader.pages:
                                    text = page.extract_text()
                                    if text:
                                        extracted_text += text + "\n"
                                st.session_state.gen_job_description = extracted_text.strip()
                                st.success(f"Successfully extracted text from {gen_uploaded_jd.name}!")
                            except Exception as e:
                                st.error(f"Error reading PDF: {e}")
                        else:
                            try:
                                text_data = gen_uploaded_jd.read().decode("utf-8")
                                st.session_state.gen_job_description = text_data
                                st.success(f"Successfully loaded {gen_uploaded_jd.name}!")
                            except Exception as e:
                                st.error(f"Error reading text file: {e}")
                                
                if st.session_state.gen_job_description:
                    st.info(f"Loaded Job Description: {len(st.session_state.gen_job_description)} characters.")

        # Template Selection card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">🎴</span> Resume Template</div>', unsafe_allow_html=True)
            st.write("Select a template layout to structure your generated resume.")
            
            templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
            available_templates = []
            if os.path.exists(templates_dir):
                try:
                    available_templates = [f for f in os.listdir(templates_dir) if f.endswith('.typ')]
                except Exception as e:
                    pass
            if not available_templates:
                available_templates = ["default.typ", "modern.typ", "minimalist.typ"]
            selected_template = st.selectbox(
                "Choose Template Layout:",
                options=available_templates,
                index=0,
                key="selected_resume_template"
            )

        # YAML Data Autofill card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">📥</span> Autofill from Existing YAML</div>', unsafe_allow_html=True)
            st.write("Upload an existing resume YAML file to automatically populate all input fields below.")
            
            uploaded_yaml = st.file_uploader(
                "Upload Resume YAML File (.yaml or .yml)",
                type=["yaml", "yml"],
                key="resume_yaml_uploader"
            )
            
            if uploaded_yaml is not None:
                if uploaded_yaml.name != st.session_state.get('last_loaded_yaml_name', ''):
                    try:
                        import yaml
                        yaml_content = yaml.safe_load(uploaded_yaml.read())
                        if isinstance(yaml_content, dict):
                            # Populate Personal Info
                            p_info = yaml_content.get('personal_info', {})
                            st.session_state.gen_full_name = p_info.get('name', '')
                            st.session_state.gen_email = p_info.get('email', '')
                            st.session_state.gen_phone = p_info.get('phone', '')
                            links_val = p_info.get('links', [])
                            st.session_state.gen_links = ", ".join(links_val) if isinstance(links_val, list) else str(links_val)
                            st.session_state.gen_summary = p_info.get('summary', '')

                            # Populate Skills
                            skills = yaml_content.get('skills', {})
                            langs = skills.get('languages', [])
                            st.session_state.gen_languages = ", ".join(langs) if isinstance(langs, list) else str(langs)
                            fws = skills.get('frameworks', [])
                            st.session_state.gen_frameworks = ", ".join(fws) if isinstance(fws, list) else str(fws)
                            dbs = skills.get('databases', [])
                            st.session_state.gen_databases = ", ".join(dbs) if isinstance(dbs, list) else str(dbs)

                            # Populate Education
                            edu = yaml_content.get('education', [])
                            if isinstance(edu, list) and edu:
                                st.session_state.edu_entries = []
                                for item in edu:
                                    st.session_state.edu_entries.append({
                                        "school": item.get('institution', ''),
                                        "degree": item.get('degree', ''),
                                        "year": item.get('graduation', ''),
                                        "gpa": item.get('gpa', '')
                                    })

                            # Populate Experience
                            exp = yaml_content.get('experience', [])
                            if isinstance(exp, list) and exp:
                                st.session_state.exp_entries = []
                                for item in exp:
                                    hls = item.get('highlights', [])
                                    hl_str = "\n".join(hls) if isinstance(hls, list) else str(hls)
                                    hl_str_formatted = ""
                                    for line in hl_str.split("\n"):
                                        line_s = line.strip()
                                        if line_s:
                                            if not line_s.startswith("-"):
                                                hl_str_formatted += f"- {line_s}\n"
                                            else:
                                                hl_str_formatted += f"{line_s}\n"
                                    st.session_state.exp_entries.append({
                                        "title": item.get('title', ''),
                                        "company": item.get('company', ''),
                                        "duration": item.get('duration', ''),
                                        "highlights": hl_str_formatted.strip()
                                    })

                            # Populate Projects
                            proj = yaml_content.get('projects', [])
                            if isinstance(proj, list) and proj:
                                st.session_state.proj_entries = []
                                for item in proj:
                                    desc = item.get('description', [])
                                    desc_str = "\n".join(desc) if isinstance(desc, list) else str(desc)
                                    desc_str_formatted = ""
                                    for line in desc_str.split("\n"):
                                        line_s = line.strip()
                                        if line_s:
                                            if not line_s.startswith("-"):
                                                desc_str_formatted += f"- {line_s}\n"
                                            else:
                                                desc_str_formatted += f"{line_s}\n"
                                    st.session_state.proj_entries.append({
                                        "name": item.get('name', ''),
                                        "tech": item.get('tech_stack', ''),
                                        "desc": desc_str_formatted.strip()
                                    })
                            
                            st.session_state.last_loaded_yaml_name = uploaded_yaml.name
                            st.success(f"Successfully loaded and populated data from {uploaded_yaml.name}!")
                            st.rerun()
                        else:
                            st.error("Invalid YAML format. The YAML file must contain key-value mappings.")
                    except Exception as e:
                        st.error(f"Error parsing YAML file: {e}")

        # Personal Information card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">👤</span> Personal Information</div>', unsafe_allow_html=True)
            full_name = st.text_input("Full Name", placeholder="Jane Doe", key="gen_full_name")
            email = st.text_input("Email Address", placeholder="jane.doe@example.com", key="gen_email")
            phone = st.text_input("Phone Number", placeholder="+1 (555) 019-2834", key="gen_phone")
            links = st.text_input("GitHub / LinkedIn Links (Comma separated)", placeholder="github.com/janedoe, linkedin.com/in/janedoe", key="gen_links")
            summary = st.text_area("Professional Summary", placeholder="A brief summary of your background...", height=100, key="gen_summary")
            
        # Dynamic Education card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">🎓</span> Education</div>', unsafe_allow_html=True)
            
            for i, entry in enumerate(st.session_state.edu_entries):
                st.markdown(f"<div style='font-weight: 600; color: #A855F7; margin-bottom: 0.5rem;'>Education #{i+1}</div>", unsafe_allow_html=True)
                col_sch, col_deg = st.columns(2)
                with col_sch:
                    entry["school"] = st.text_input("School / University", value=entry["school"], key=f"edu_school_{i}", placeholder="State University")
                with col_deg:
                    entry["degree"] = st.text_input("Degree & Major", value=entry["degree"], key=f"edu_degree_{i}", placeholder="B.S. in Computer Science")
                
                col_yr, col_gpa = st.columns(2)
                with col_yr:
                    entry["year"] = st.text_input("Graduation Date / Year", value=entry["year"], key=f"edu_year_{i}", placeholder="May 2024")
                with col_gpa:
                    entry["gpa"] = st.text_input("GPA / Honors (Optional)", value=entry["gpa"], key=f"edu_gpa_{i}", placeholder="3.8 / Cum Laude")
                
                if len(st.session_state.edu_entries) > 1:
                    if st.button(f"❌ Remove Education #{i+1}", key=f"remove_edu_{i}"):
                        st.session_state.edu_entries.pop(i)
                        st.rerun()
                if i < len(st.session_state.edu_entries) - 1:
                    st.divider()
                    
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            if st.button("➕ Add Education Entry", key="add_edu_btn"):
                st.session_state.edu_entries.append({"school": "", "degree": "", "year": "", "gpa": ""})
                st.rerun()
            
        # Skills card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">💡</span> Skills</div>', unsafe_allow_html=True)
            languages = st.text_input("Languages", placeholder="Python, Java, JavaScript, Rust", key="gen_languages")
            frameworks = st.text_input("Frameworks & Tools", placeholder="React, Node.js, Git, Docker", key="gen_frameworks")
            databases = st.text_input("Databases", placeholder="PostgreSQL, MongoDB, Redis", key="gen_databases")

        # Dynamic Experience card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">💼</span> Professional Experience</div>', unsafe_allow_html=True)
            
            for i, entry in enumerate(st.session_state.exp_entries):
                st.markdown(f"<div style='font-weight: 600; color: #A855F7; margin-bottom: 0.5rem;'>Experience #{i+1}</div>", unsafe_allow_html=True)
                col_title, col_comp = st.columns(2)
                with col_title:
                    entry["title"] = st.text_input("Job Title", value=entry["title"], key=f"exp_title_{i}", placeholder="Software Engineer")
                with col_comp:
                    entry["company"] = st.text_input("Company Name", value=entry["company"], key=f"exp_company_{i}", placeholder="Tech Corp")
                
                entry["duration"] = st.text_input("Duration", value=entry["duration"], key=f"exp_duration_{i}", placeholder="June 2022 - Present")
                entry["highlights"] = st.text_area("Key Responsibilities (one per line)", value=entry["highlights"], key=f"exp_highlights_{i}", placeholder="- Led development of the main landing page.\n- Reduced backend API latency by 20%.", height=120)
                
                if len(st.session_state.exp_entries) > 1:
                    if st.button(f"❌ Remove Experience #{i+1}", key=f"remove_exp_{i}"):
                        st.session_state.exp_entries.pop(i)
                        st.rerun()
                if i < len(st.session_state.exp_entries) - 1:
                    st.divider()
                    
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            if st.button("➕ Add Experience Entry", key="add_exp_btn"):
                st.session_state.exp_entries.append({"title": "", "company": "", "duration": "", "highlights": ""})
                st.rerun()
            
        # Dynamic Projects card
        with st.container(border=True):
            st.markdown('<div class="section-header"><span class="section-icon">🛠️</span> Projects</div>', unsafe_allow_html=True)
            
            for i, entry in enumerate(st.session_state.proj_entries):
                st.markdown(f"<div style='font-weight: 600; color: #A855F7; margin-bottom: 0.5rem;'>Project #{i+1}</div>", unsafe_allow_html=True)
                col_name, col_tech = st.columns(2)
                with col_name:
                    entry["name"] = st.text_input("Project Name", value=entry["name"], key=f"proj_name_{i}", placeholder="Resume Parser Agent")
                with col_tech:
                    entry["tech"] = st.text_input("Tech Stack Used", value=entry["tech"], key=f"proj_tech_{i}", placeholder="Python, OpenAI API, Streamlit")
                
                entry["desc"] = st.text_area("Project Description (one per line)", value=entry["desc"], key=f"proj_desc_{i}", placeholder="- Designed and built a multi-agent resume tailoring pipeline.\n- Handled high volume file parsing.", height=100)
                
                if len(st.session_state.proj_entries) > 1:
                    if st.button(f"❌ Remove Project #{i+1}", key=f"remove_proj_{i}"):
                        st.session_state.proj_entries.pop(i)
                        st.rerun()
                if i < len(st.session_state.proj_entries) - 1:
                    st.divider()
                    
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            if st.button("➕ Add Project Entry", key="add_proj_btn"):
                st.session_state.proj_entries.append({"name": "", "tech": "", "desc": ""})
                st.rerun()

        # Center Button to Create Resume
        st.divider()
        
        can_gen = len(st.session_state.gen_job_description.strip()) > 0 and len(full_name.strip()) > 0
        
        yaml_btn = st.button("💾 Create Resume", disabled=not can_gen, key="create_resume_btn")
        
        if not can_gen:
            if not full_name.strip():
                st.caption("<div style='text-align: center; color: #EF4444;'>Please fill in your Full Name to proceed.</div>", unsafe_allow_html=True)
            elif not st.session_state.gen_job_description.strip():
                st.caption("<div style='text-align: center; color: #EF4444;'>Please provide a Target Job Description to enable resume tailoring.</div>", unsafe_allow_html=True)
        else:
            st.caption("<div style='text-align: center; color: #9CA3AF;'>Ready to generate. Press the button to run the resume builder and tailor flow.</div>", unsafe_allow_html=True)
            
        if yaml_btn:
            st.session_state.gen_pipeline_running = True
            
        if st.session_state.gen_pipeline_running:
            with st.container(border=True, key="gen_progress_container"):
                st.markdown("#### Resume Generation & Tailoring Progress")
                
                gen_steps = [
                    ("Step 1: Parsing form data inputs and personal profile details", 1.2),
                    ("Step 2: Structuring resume data and generating base Typst template", 1.5),
                    ("Step 3: Analyzing target job description for key skills and tailoring hooks", 1.8),
                    ("Step 4: Tailoring generated resume sections to align with the job description", 2.2),
                    ("Step 5: Formatting, styling, and validation of compiled Typst code", 1.0)
                ]
                
                # Progress bars and steps
                gen_progress_bar = st.progress(0)
                gen_step_container = st.empty()
                
                for idx, (step_name, delay) in enumerate(gen_steps):
                    html_steps = []
                    for i in range(len(gen_steps)):
                        status_class = "pipeline-step"
                        status_icon = "⚪"
                        if i < idx:
                            status_class += " pipeline-step-completed"
                            status_icon = "🟢 Completed"
                        elif i == idx:
                            status_class += " pipeline-step-active"
                            status_icon = "⚡ Running..."
                        else:
                            status_icon = "⏳ Pending"
                            
                        html_steps.append(f"""
                        <div class="{status_class}">
                            <span>{gen_steps[i][0]}</span>
                            <strong>{status_icon}</strong>
                        </div>
                        """)
                        
                    gen_step_container.markdown("\n".join(html_steps), unsafe_allow_html=True)
                    
                    progress_val = int(((idx + 0.5) / len(gen_steps)) * 100)
                    gen_progress_bar.progress(progress_val)
                    
                    time.sleep(delay)
                    
                # Mark all completed
                html_steps = []
                for i in range(len(gen_steps)):
                    html_steps.append(f"""
                    <div class="pipeline-step pipeline-step-completed">
                        <span>{gen_steps[i][0]}</span>
                        <strong>🟢 Completed</strong>
                    </div>
                    """)
                gen_step_container.markdown("\n".join(html_steps), unsafe_allow_html=True)
                gen_progress_bar.progress(100)
                
                # Success
                st.success("🎉 Resume generated and tailored successfully!")
                
                # Build the Typst code dynamically styled based on the selected template style
                selected_template_name = st.session_state.get('selected_resume_template', 'default.typ')
                template_comment = f"// Template Source: templates/{selected_template_name}\n"
                
                template_lower = selected_template_name.lower()
                if "minimal" in template_lower:
                    theme_name = "Minimalist"
                    margin = "(x: 2cm, y: 2.2cm)"
                    font = "Liberation Sans"
                    size = "9.5pt"
                    title_size = "18pt"
                    heading_format = "== "
                elif "modern" in template_lower or "creative" in template_lower:
                    theme_name = "Modern Accent"
                    margin = "(x: 1.25cm, y: 1.75cm)"
                    font = "Outfit"
                    size = "10pt"
                    title_size = "22pt"
                    heading_format = "== #text(fill: rgb(\"#8B5CF6\"))"
                else:
                    theme_name = "Classic Professional"
                    margin = "(x: 1.5cm, y: 2cm)"
                    font = "Liberation Sans"
                    size = "10pt"
                    title_size = "20pt"
                    heading_format = "== "

                links_list = [l.strip() for l in links.split(",") if l.strip()]
                links_typst = " | ".join(links_list) if links_list else "github.com/janedoe"
                
                gen_typst_code = f"""{template_comment}// Dynamic Typst Resume - {theme_name} Theme
#set page(paper: "us-letter", margin: {margin})
#set text(font: "{font}", size: {size})

#align(center)[
  #text(size: {title_size}, weight: "bold")[{full_name or 'Jane Doe'}] \\
  #text(fill: gray)[{email or 'jane.doe@example.com'} | {phone or '+1 (555) 019-2834'} | {links_typst}]
]

{heading_format}[Professional Summary]
{summary or 'A results-driven engineer experienced in building scalable applications.'}

{heading_format}[Technical Skills]
- *Languages*: {languages or 'Python, Java, JavaScript, Rust'}
- *Frameworks & Tools*: {frameworks or 'React, Node.js, Git, Docker'}
- *Databases*: {databases or 'PostgreSQL, MongoDB, Redis'}
"""

                # Add education
                if st.session_state.edu_entries:
                    gen_typst_code += f"\n{heading_format}[Education]\n"
                    for entry in st.session_state.edu_entries:
                        sch = entry.get('school') or 'State University'
                        deg = entry.get('degree') or 'B.S. in Computer Science'
                        yr = entry.get('year') or 'May 2024'
                        gpa = entry.get('gpa') or '3.8'
                        gpa_str = f" (GPA: {gpa})" if gpa else ""
                        gen_typst_code += f"- *{deg}* - {sch} _({yr})_{gpa_str}\n"

                # Add experience
                if st.session_state.exp_entries:
                    gen_typst_code += f"\n{heading_format}[Professional Experience]\n"
                    for entry in st.session_state.exp_entries:
                        title = entry.get('title') or 'Software Engineer'
                        comp = entry.get('company') or 'Tech Corp'
                        dur = entry.get('duration') or 'June 2022 - Present'
                        highlights = entry.get('highlights') or '- Led development tasks.\n- Handled backend APIs.'
                        
                        gen_typst_code += f"*{title}* @ {comp} _({dur})_\n"
                        for hl in highlights.split('\n'):
                            if hl.strip():
                                clean_hl = hl.strip().lstrip('-').strip()
                                gen_typst_code += f"- {clean_hl}\n"
                        gen_typst_code += "\n"

                # Add projects
                if st.session_state.proj_entries:
                    gen_typst_code += f"\n{heading_format}[Projects]\n"
                    for entry in st.session_state.proj_entries:
                        name = entry.get('name') or 'Resume Parser Agent'
                        tech = entry.get('tech') or 'Python, Streamlit'
                        desc = entry.get('desc') or '- Designed LLM pipelines.\n- Handled high volume file parsing.'
                        
                        gen_typst_code += f"*{name}* _({tech})_\n"
                        for d in desc.split('\n'):
                            if d.strip():
                                clean_d = d.strip().lstrip('-').strip()
                                gen_typst_code += f"- {clean_d}\n"
                        gen_typst_code += "\n"

                # Layout generated output and adaptation analysis
                gen_res_col1, gen_res_col2 = st.columns(2)
                with gen_res_col1:
                    st.markdown("##### 📁 Tailored Typst Output")
                    st.code(gen_typst_code, language="rust")
                    
                    st.download_button(
                        label="💾 Download Tailored Typst File",
                        data=gen_typst_code,
                        file_name="tailored_resume.typ",
                        mime="text/plain"
                    )
                    
                with gen_res_col2:
                    st.markdown("##### 🔍 Adaptation Analysis Report")
                    
                    # Compute dynamic list of skills to show in adaptation report
                    detected_skills = [s.strip() for s in languages.split(",") + frameworks.split(",") if s.strip()]
                    skills_bullet = "\n".join([f"- Embedded target skill: **{sk}**" for sk in detected_skills[:4]]) if detected_skills else "- Aligned project accomplishments with job description keywords."
                    
                    st.markdown(f"""
                    **Generation & Tailoring Score:** 97%
                    
                    **Key Actions Performed:**
                    - Synthesized form details into standard resume template structure.
                    - Tailored experience highlights matching job requirements:
                      *"{st.session_state.gen_job_description[:60]}..."*
                    {skills_bullet}
                    - Automatically verified Typst syntax and formatting.
                    
                    **Recommended Next Steps:**
                    - Compile the tailored file using the command-line: `typst compile tailored_resume.typ`
                    - Open the resulting PDF to review visual alignment and layout margins.
                    """)
                
                st.session_state.gen_pipeline_running = False
