import os

API_BASE_URL = os.getenv(
    "EQUIP_API_URL",
    "http://127.0.0.1:8000/api"
)

APP_NAME = "Chemical Equipment Analyzer"
APP_VERSION = "1.0.0"
TOKEN_URL = f"{API_BASE_URL}/token/"

MAX_HISTORY_ITEMS = 5
