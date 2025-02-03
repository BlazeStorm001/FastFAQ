from app.utils.lang_utils import translate_text, check_language_code
from sqlalchemy.orm import Session
from app.models.faq import FAQ, FAQTranslation
from app.config import DEFAULT_LANGUAGES
from app.schemas.faq import FAQCreate
from fastapi import HTTPException
from typing import List, Optional


def create_faq(db: Session, faq: FAQCreate) -> FAQ:

    if not check_language_code(faq.language):
        raise HTTPException(status_code=400, detail="Invalid language format. Use a two-letter code (e.g., 'en', 'fr').")

    # Insert into FAQ table
    new_faq = FAQ(question=faq.question, answer=faq.answer, language=faq.language)
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)

    # Insert translations into FAQTranslation table
    for lang in DEFAULT_LANGUAGES:
        if lang != faq.language:
            # Translate the question and answer directly including HTML
            translated_question = translate_text(faq.question, lang)
            translated_answer = translate_text(faq.answer, lang)

            # print(f"Translated question ({lang}): {translated_question}")
            # print(f"Translated answer ({lang}): {translated_answer}")
            # from pdb import set_trace
            # set_trace()

            # Create and insert the translation entry
            faq_translation = FAQTranslation(
                faq_id=new_faq.id,
                language=lang,
                question=translated_question,
                answer=translated_answer
            )
            db.add(faq_translation)

    db.commit()
    return new_faq

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
    if id:
        # Fetch a specific FAQ by ID and language
        faq = db.query(FAQ).filter(FAQ.id == id).first()

        if not faq:
            return []

        if faq.language == lang:
            return [faq]


        if faq.language != lang:
            # Fetch translation if requested language is different from the FAQ language
            translation = db.query(FAQTranslation).filter(FAQTranslation.faq_id == id, FAQTranslation.language == lang).first()
            if not translation:
                if faq.language == 'en':
                    return [faq]
                else:
                    translation = db.query(FAQTranslation).filter(FAQTranslation.faq_id == id, FAQTranslation.language == 'en').first()

            faq = FAQ(id=id, question=translation.question, answer=translation.answer, language=lang)
            return [faq] if faq else []

    else:
        # Fetch all FAQs in the requested language
        faqs = db.query(FAQ).all()

        result = []

        for faq in faqs:

            if faq.language == lang:
                result.append(faq)
            else:
                translation = db.query(FAQTranslation).filter(FAQTranslation.faq_id == faq.id, FAQTranslation.language == lang).first()
                if not translation:
                    if faq.language == 'en':
                        result.append(faq)
                        continue
                    else:
                        translation = db.query(FAQTranslation).filter(FAQTranslation.faq_id == faq.id, FAQTranslation.language == 'en').first()
                result.append(FAQ(id=faq.id, question=translation.question, answer=translation.answer, language=lang))


        return result
