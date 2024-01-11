import os
from chromadb.config import Settings

# Define the folder for storing database
cwd = os.getcwd()
persist_db = os.environ.get('PERSIST_DIRECTORY', 'db')

PERSIST_DIRECTORY = f'{cwd}/auto_job_app/{persist_db}'

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    persist_directory=PERSIST_DIRECTORY,
    anonymized_telemetry=False
)
