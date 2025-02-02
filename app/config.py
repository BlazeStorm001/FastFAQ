from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
