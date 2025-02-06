from sqlalchemy.orm import Session
from app.models.faq import FAQ
from app.schemas.faq import FAQCreate
from fastapi import HTTPException
from fastapi import BackgroundTasks
from .delete import delete_faq
from .create import create_faq


def update_faq(db: Session, id: int, faq: FAQCreate, background_tasks: BackgroundTasks) -> FAQ:

    # Check if the FAQ exists
    existing_faq = db.query(FAQ).filter(FAQ.id == id, FAQ.language == faq.language).first()

    if not existing_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    if faq.question == existing_faq.question and faq.answer == existing_faq.answer:
        return existing_faq

    # Delete the existing FAQ and translations
    delete_faq(db, id)

    return create_faq(db, faq, background_tasks, id)
