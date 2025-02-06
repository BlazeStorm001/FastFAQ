from sqlalchemy.orm import Session
from app.models.faq import FAQ, FAQTranslation
from typing import List, Optional
from app.caching import get_faqs_from_cache, add_faqs_to_cache


def get_faqs(db: Session, id: Optional[int] = None, lang: str = 'en') -> List[FAQ]:
    """
    Fetch FAQ(s) from the database based on language.

    Args:
        db: Database session.
        id: FAQ ID (optional, if None, fetch all FAQs).
        lang: Language for filtering FAQs.

    Returns:
        A list of FAQs.
    """
    cached_entries = get_faqs_from_cache(id=id, lang=lang)
    if cached_entries:
        return cached_entries

    if id:
        return get_faq_by_id(db, id, lang)
    else:
        return get_all_faqs(db, lang)


def get_faq_by_id(db: Session, id: int, lang: str) -> List[FAQ]:
    """Fetch a specific FAQ by ID, with translation handling."""
    faq = db.query(FAQ).filter(FAQ.id == id).first()
    if not faq:
        return []

    if faq.language == lang:
        return [faq]

    return [get_faq_translation(db, faq, lang)]


def get_faq_translation(db: Session, faq: FAQ, lang: str) -> FAQ:
    """Fetch the translation of an FAQ. Defaults to English if the requested language is missing."""
    translation = db.query(FAQTranslation).filter(FAQTranslation.faq_id == faq.id, FAQTranslation.language == lang).first()

    if not translation:
        if faq.language == 'en':
            return faq
        translation = db.query(FAQTranslation).filter(FAQTranslation.faq_id == faq.id, FAQTranslation.language == 'en').first()

    return FAQ(id=faq.id, question=translation.question, answer=translation.answer, language=lang)


def get_all_faqs(db: Session, lang: str) -> List[FAQ]:
    """Fetch all FAQs in the requested language, handling translations."""
    faqs = db.query(FAQ).all()
    result = []

    for faq in faqs:
        if faq.language == lang:
            result.append(faq)
        else:
            result.append(get_faq_translation(db, faq, lang))

    add_faqs_to_cache(result)
    return result
