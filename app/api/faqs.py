from fastapi import APIRouter
from fastapi import Depends
from app.schemas.faq import FAQCreate, FAQ
from app.crud.faq import create_faq
from app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/faqs/", response_model=FAQ, status_code=201)
def create_faq_endpoint(faq: FAQCreate, db: Session = Depends(get_db)):
    return create_faq(db, faq)