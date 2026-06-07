import os
from dotenv import load_dotenv

load_dotenv()

# Server Configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"

# Processing Configuration
DEFAULT_INTENSITY = os.getenv("DEFAULT_INTENSITY", "medium")
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", 100))
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", 10000))

# Intensity Levels Configuration
INTENSITY_LEVELS = {
    "light": {
        "description": "Minimal changes, preserves original meaning",
        "parameters": {
            "phrase_variation": 0.3,
            "synonym_replacement": 0.2,
            "sentence_reorder": 0.1
        }
    },
    "medium": {
        "description": "Balanced transformation",
        "parameters": {
            "phrase_variation": 0.6,
            "synonym_replacement": 0.4,
            "sentence_reorder": 0.3
        }
    },
    "strong": {
        "description": "Significant rewording",
        "parameters": {
            "phrase_variation": 0.9,
            "synonym_replacement": 0.7,
            "sentence_reorder": 0.6
        }
    }
}
