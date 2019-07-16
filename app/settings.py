import os
from pathlib import Path

BASE_DIR = Path(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = BASE_DIR / "data"

DEBUG = True  # Note: Use DEBUG = False in production
