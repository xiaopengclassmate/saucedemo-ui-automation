import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")
STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
PASSWORD = os.getenv("PASSWORD", "secret_sauce")
DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "10000"))
NAVIGATION_TIMEOUT_MS = int(os.getenv("NAVIGATION_TIMEOUT_MS", "30000"))
