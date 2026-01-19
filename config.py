import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config: 
    SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY", "")