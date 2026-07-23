import os
from openai import OpenAI

def get_llm_client():
    # Communicate with Ollama locally using the OpenAI Python SDK
    base_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434/v1")
    return OpenAI(
        base_url=base_url,
        api_key="ollama"  # Required by the SDK but ignored by Ollama
    )

def get_default_model():
    return os.environ.get("LLM_MODEL", "qwen2.5:1.5b")
