from fastapi import FastAPI
from app.database.session import engine, Base
from app.models.faq import FAQ, FAQTranslation

# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FAQ API"}
