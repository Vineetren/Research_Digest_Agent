import os
from dotenv import load_dotenv

load_dotenv()

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.85))
MIN_CONTENT_LENGTH = int(os.getenv("MIN_CONTENT_LENGTH", 200))
MAX_CLAIMS_PER_SOURCE = int(os.getenv("MAX_CLAIMS_PER_SOURCE", 5))

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
CHAT_MODEL = os.getenv("CHAT_MODEL")
