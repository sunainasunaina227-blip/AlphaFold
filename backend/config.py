import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Use GEMINI_API_KEY for Live Chat as it supports the Live API and has active credits
GEMINI_LIVE_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_FAST = "gemini-3.5-flash"      # For scoring, pattern mapping
GEMINI_MODEL_QUALITY = "gemini-3.1"          # For extraction, summaries
GEMINI_MODEL = GEMINI_MODEL_FAST             # Default model to use

# MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "")

# Google OAuth
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# Upload limits
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "100"))

# Supported file extensions
SUPPORTED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".webm"}
SUPPORTED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov"}
SUPPORTED_DOC_EXTENSIONS = {".docx"}
SUPPORTED_TEXT_EXTENSIONS = {".txt"}

ALL_SUPPORTED_EXTENSIONS = (
    SUPPORTED_AUDIO_EXTENSIONS
    | SUPPORTED_VIDEO_EXTENSIONS
    | SUPPORTED_DOC_EXTENSIONS
    | SUPPORTED_TEXT_EXTENSIONS
)
