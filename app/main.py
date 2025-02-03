from app.database.session import engine, Base
from fastapi import FastAPI
from app.api import faqs


# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)



app.include_router(faqs.router, prefix="/api", tags=["FAQs"])


