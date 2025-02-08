from app.database.session import engine, Base
from fastapi import FastAPI
from app.api import faqs
from app.middleware import add_cors_middleware

# Initialize FastAPI app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

add_cors_middleware(app)

app.include_router(faqs.router, prefix="/api", tags=["FAQs"])


