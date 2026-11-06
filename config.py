import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")

if not db_password:
    raise ValueError("DB_PASSWORD is missing from .env file")

if not secret_key:
    raise ValueError("SECRET_KEY is missing from .env file")


class Config:
    SECRET_KEY = secret_key

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://root:{quote_plus(db_password)}@localhost/campusqueue"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False