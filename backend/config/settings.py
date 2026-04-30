import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend/.env explicitly
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    """
    Configuration settings for the application.
    Never hardcodes API keys.
    """
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Feature flags
    ENABLE_BACKEND_TTS: bool = os.getenv("ENABLE_BACKEND_TTS", "false").lower() == "true"
    
    def __init__(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it in the .env file.")

settings = Settings()
