import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD", ""))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "campusqueue-dev-key")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{password}@localhost/campusqueue"
    SQLALCHEMY_TRACK_MODIFICATIONS = False