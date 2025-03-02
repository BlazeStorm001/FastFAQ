from fastapi import APIRouter
from fastapi import Depends
from app.schemas.faq import FAQCreate, FAQ
from app.crud.faqs.create import create_faq
from app.crud.faqs.read import get_faqs
from app.crud.faqs.delete import delete_faq
from app.crud.faqs.update import update_faq
from app.dependencies import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException
from typing import Optional
from fastapi import BackgroundTasks

router = APIRouter()


@router.post("/faqs/", response_model=FAQ, status_code=201)
def create_faq_endpoint(faq: FAQCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return create_faq(db, faq, background_tasks)


@router.get("/faqs/", response_model=List[FAQ])
def get_faqs_by_id_and_language(id: Optional[int] = None, lang: str = 'en', db: Session = Depends(get_db)):
    """
    Retrieve FAQs by ID and language.
    If the FAQ is not found in the requested language, an English translation is returned.
    """
    faqs = get_faqs(db, id=id, lang=lang)
    if not faqs:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faqs

@router.delete("/faqs/{id}", status_code=204)
def delete_faq_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_faq(db, id)

@router.put("/faqs/{id}", response_model=FAQ)
def update_faq_endpoint(id: int, faq: FAQCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    return update_faq(db, id, faq, background_tasks)
