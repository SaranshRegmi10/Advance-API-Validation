import os
from dotenv import load_dotenv

class Config:
    """Loads and exposes environment settings for the framework."""
    
    @classmethod
    def load_environment(cls, env_name: str = "dev"):
        # Constructing filename based on selected environment
        env_file = f".env.{env_name.lower()}"
        
        if os.path.exists(env_file):
            load_dotenv(dotenv_path=env_file, override=True)
            print(f"\n[CONFIG] Loaded environment file: {env_file}")
        else:
            print(f"\n[CONFIG] Warning: {env_file} not found. Falling back to default environment variables.")

        # Reading the environment variables with fallback defaults
        cls.BASE_URL = os.getenv("BASE_URL", "https://reqres.in")
        cls.API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
        cls.DEFAULT_USER_EMAIL = os.getenv("DEFAULT_USER_EMAIL", "eve.holt@reqres.in")
        cls.API_KEY = os.getenv("API_KEY","")