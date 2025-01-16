# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # You can load these values from environment variables for flexibility
    # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost/monitoring_tool")
    DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL", "postgresql://user:password@localhost/test_db")

settings = Settings()
