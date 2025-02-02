from app.database.session import engine, Base
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.faq import FAQCreate, FAQ
from app.crud.faq import create_faq

# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.post("/faqs/", response_model=FAQ)
def create_faq_endpoint(faq: FAQCreate, db: Session = Depends(get_db)):
    return create_faq(db, faq)





