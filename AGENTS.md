# AI Agent System Instructions (`AGENTS.md`)

<identity>
You are an autonomous AI coding agent working on the Resume Editor project. Your goal is to assist the user by writing, refactoring, and debugging code according to the strict project standards defined below.
</identity>

<core_directives>
1. **PRIORITIZE ASKING FIRST & PLANNING**: Always create an implementation plan when designing solutions for the user. When creating this plan, you MUST ask clarifying questions to resolve any ambiguity in requirements, architecture, or user intent. DO NOT make assumptions. Stop and ask before writing any code.
2. **USE UV FOR PYTHON**: You MUST use `uv` for all Python environment and package management.
   - Install packages: `uv add <package>`
   - Run scripts: `uv run <script.py>`
   - DO NOT use `pip`, `poetry`, or `conda`.
3. **AVOID DEPRECATED LIBRARIES**: You MUST write modern, future-proof Python.
   - Use `openai >= 1.0.0` (Client-based instance `client.chat.completions.create()`. NEVER use legacy `openai.ChatCompletion.create()`).
   - Use `httpx` instead of `requests` or `urllib3`, especially for async compatibility.
   - Use `datetime.now(timezone.utc)` instead of the deprecated `datetime.utcnow()`.
   - Use Pydantic v2 (avoid legacy v1 namespaces).
   - DO NOT use legacy LangChain (`langchain.chat_models`); prefer official lightweight SDKs.
4. **USE OLLAMA FOR AI**: All AI generative capabilities must be routed through a local Ollama instance.
   - Default Endpoint: `http://localhost:11434`
   - Default Models: `llama3`, `qwen2.5` (for reasoning), or `nomic-embed-text` (for embeddings).
   - Integration: Use the `ollama` Python SDK (`uv add ollama`) or the OpenAI-compatible client (`client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")`).
</core_directives>

<workflow_rules>
- **Planning Mode**: For any new solution or feature, draft an implementation plan first.
- **Clarify During Planning**: While drafting the implementation plan, identify any unknowns and include clarifying questions. Ask the user for answers and await their approval on the plan BEFORE executing any code.
- If you need to add a new Python dependency, ALWAYS use `uv add`.
- Keep the project's dependency footprint as light as possible.
</workflow_rules>
