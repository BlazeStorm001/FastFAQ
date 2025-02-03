# Dependency to get the database session
from app.database.session import SessionLocal
from google.cloud import translate_v2 as translate
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize Google Translate client once
translate_client = translate.Client()
