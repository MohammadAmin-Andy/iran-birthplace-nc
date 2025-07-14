# backend/app/config.py

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Manages application settings and configurations.
    It automatically reads environment variables.
    """
    PROJECT_NAME: str = "Iran Birthplace National Code API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "An open-source API to validate Iranian national codes based on birthplace codes."
    
    # Path to the JSON dataset
    # It constructs the path relative to this file's location.
    # __file__ -> config.py
    # os.path.dirname(...) -> app/
    # os.path.join(..., 'data', 'national_codes.json') -> app/data/national_codes.json
    DATASET_PATH: str = os.path.join(os.path.dirname(__file__), 'data', 'national_codes.json')

    class Config:
        # This allows pydantic to look for a .env file and load variables from it.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single, reusable instance of the settings
settings = Settings()