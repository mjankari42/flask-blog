import os
from pathlib import Path

base_directory = Path(__file__).parent
default_db = f"sqlite:///{Path(base_directory) / 'app.db'}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-password-safe"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or default_db

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["your-email@example.com"]

    POSTS_PER_PAGE = 3
