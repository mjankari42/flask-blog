import os
from pathlib import Path

base_directory = Path(__file__).parent
default_db = f"sqlite:///{Path(base_directory) / 'app.db'}"

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-password-safe"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_db
