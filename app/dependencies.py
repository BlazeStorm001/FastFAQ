# Dependency to get the database session
from app.database.session import SessionLocal
from google.cloud import translate_v2 as translate
from app.config import REDIS_HOST, REDIS_PORT
import redis

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize Google Translate client once
translate_client = translate.Client()

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
