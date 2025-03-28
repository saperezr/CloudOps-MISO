import os
from dotenv import load_dotenv

load_dotenv(".env")

class Config:    
    def build_db_string_connection():
      return f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = build_db_string_connection()
    JWT_SECRET_KEY = "blacklist_app_devops"