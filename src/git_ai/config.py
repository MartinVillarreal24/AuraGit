import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env if it exists
load_dotenv()

# Load global .env from home directory as fallback
global_config_path = Path.home() / ".git-ai" / ".env"
if global_config_path.exists():
    load_dotenv(dotenv_path=global_config_path, override=False)

class Config:
    # General Settings
    AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama").lower()  # ollama, openai, gemini, anthropic
    COMMIT_STYLE = os.getenv("COMMIT_STYLE", "conventional")
    AI_LANGUAGE = os.getenv("AI_LANGUAGE", "en").lower()  # en, es
    
    # Ollama Settings
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Gemini Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    
    # Anthropic Settings
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")

    @classmethod
    def validate(cls):
        """Validates that necessary keys are present for the selected provider."""
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing in .env")
        if cls.AI_PROVIDER == "gemini" and not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing in .env")
        if cls.AI_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is missing in .env")
