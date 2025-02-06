from sqlalchemy.orm import Session
from app.models.faq import FAQ, FAQTranslation
from fastapi import HTTPException
from app.caching import flush_all_faqs

def delete_faq(db: Session, id: int) -> None:
    """Delete an FAQ by ID."""
    faq = db.query(FAQ).filter(FAQ.id == id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    db.query(FAQTranslation).filter(FAQTranslation.faq_id == id).delete(synchronize_session=False)
    db.delete(faq)
    db.commit()
    flush_all_faqs()
