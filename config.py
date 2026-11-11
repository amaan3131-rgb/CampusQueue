
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
secret_key = os.getenv("SECRET_KEY")

if not all([db_host, db_user, db_password, db_name, secret_key]):
    raise ValueError("One or more required environment variables are missing.")

class Config:
    SECRET_KEY = secret_key

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{quote_plus(db_user)}:"
        f"{quote_plus(db_password)}@{db_host}:3306/{db_name}"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "ssl": {}
        }
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = True
