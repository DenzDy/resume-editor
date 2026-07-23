# Multi-Agent Resume Editor

An AI-powered tool designed to autonomously tailor your resume to match specific job descriptions using locally hosted LLMs. 

Unlike standard text editors, this system safely parses and edits your resume in **Typst** format (`.typ`), ensuring that the structural layout remains perfectly intact while the content is intelligently rewritten. 

## Features

- **Multi-Agent Architecture**: 
  - **Editor Agent**: Isolates your Experience section, identifies gaps based on the Job Description, and interacts with you (asking clarifying questions) to draw out missing, relevant truthful details.
  - **Screener Agent**: Runs in a completely isolated context (acting as an HR verifier) to score the updated resume against the job description (0-100 Match Score).
- **Web Scraping Support**: Integrated with Playwright to seamlessly fetch job descriptions directly from JavaScript-heavy job boards like LinkedIn or Workday.
- **Dual Interfaces**: Use the lightning-fast CLI or the visual Streamlit web interface.
- **Agent Skill Included**: Natively integrated with Gemini/Claude Code CLI through the provided `.skill.md` definition.
- **Local AI execution**: All agent intelligence runs locally via Ollama. 

---

## Getting Started

### Prerequisites
- **Python 3.12+**
- **Ollama**: Must be installed and running locally on `http://localhost:11434` (Default model: `qwen2.5:1.5b` or configure via `LLM_MODEL`).
- **`uv`**: We use Astral's `uv` for lightning-fast dependency management.

### Installation

#### 1. Install Ollama & Local Models
Since all AI inference runs locally for privacy, you must install Ollama:
- **macOS / Linux / WSL**: `curl -fsSL https://ollama.com/install.sh | sh`
- **Windows**: Download the installer from [ollama.com](https://ollama.com)
  
Once installed, make sure the service is running, then pull the default model (this might take a few minutes to download):
```bash
ollama run qwen2.5:1.5b
```

#### 2. Install `uv` & Setup Environment
We use Astral's `uv` for lightning-fast dependency management and virtual environments.

1. **Install `uv`** (if you don't have it):
   ```bash
   curl -FsSL https://astral.sh/uv/install.sh | sh
   source $HOME/.cargo/env
   ```
2. **Create and Activate Virtual Environment**:
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. **Sync Dependencies**:
   ```bash
   uv sync
   ```
4. **Install Playwright Browsers** (Required for scraping job links):
   ```bash
   uv run playwright install chromium
   ```

---

## Usage

Make sure your Ollama instance is running in the background before starting the application.

### 1. Web UI Mode (Graphical App)
The Streamlit web interface is the easiest way to visually edit your resume and see the updated Typst code instantly.
Launch the graphical interface:
```bash
uv run streamlit run app.py
```
- **Step 1**: Open your browser to the local URL provided by Streamlit.
- **Step 2**: Paste your Typst code (`.typ`) into the left input box.
- **Step 3**: Provide a Job Description URL or paste the raw text into the right input box.
- **Step 4**: Click **Analyze & Edit**. The UI will orchestrate the Editor and Screener agents and output your newly formatted `.typ` code alongside your Match Score.

### 2. CLI Mode (Interactive Terminal)
For standard terminal-based interactions. In CLI mode, the Editor Agent can actively prompt you with clarifying questions to extract better information.
Launch the CLI orchestrator:
```bash
uv run main.py
```
- **Step 1**: You will be prompted to provide the path to your `.typ` file.
- **Step 2**: Enter the Job Description URL (it will be scraped automatically) or paste the raw text.
- **Step 3**: The Editor Agent will analyze the gap. **If it needs more information about your experience, it will pause and ask you directly in the terminal!**
- **Step 4**: Provide your answers. The system will then generate your new `_updated.typ` file and display the final Match Score.

### 3. Agent Skill Mode (Gemini/Claude Code CLI)
If you are using an AI CLI (like Gemini IDE or Claude Code), you can load the included `resume_editor.skill.md` file so the AI agent natively understands how to perform this workflow for you.
- **Step 1**: Copy the `resume_editor.skill.md` file into your AI's standard skills directory (e.g., `~/.gemini/config/skills/`).
- **Step 2**: In your AI chat interface, trigger the workflow by asking (e.g., *"Use the Resume Editor to tailor my resume"*).
- **Step 3**: The AI agent will read the skill instructions, execute the scripts natively, interact with you directly in the chat if details are missing, and present the final results natively!

---

## Project Structure

- `AGENTS.md` - Strict system instructions and guardrails for future AI agents working on this codebase.
- `pyproject.toml` - `uv` dependency configuration.
- `llm_client.py` - Core Ollama connection wrapper.
- `agents/editor.py` - The Editor Sub-Agent logic.
- `agents/screener.py` - The Screener Sub-Agent logic.
- `utils/typst_parser.py` - Regex-based Typst extraction and injection logic.
- `utils/web_scraper.py` - Playwright & HTTPX fallback logic for job fetching.
- `resume_editor.skill.md` - Agent instruction definitions.
