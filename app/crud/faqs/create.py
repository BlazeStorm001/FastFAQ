from app.utils.lang_utils import translate_text, check_language_code
from sqlalchemy.orm import Session
from app.models.faq import FAQ, FAQTranslation
from app.config import DEFAULT_LANGUAGES
from app.schemas.faq import FAQCreate
from fastapi import HTTPException
from app.caching import flush_all_faqs
from fastapi import BackgroundTasks



def create_faq(db: Session, faq: FAQCreate, background_tasks: BackgroundTasks, id: int = None) -> FAQ:

    if not check_language_code(faq.language):
        raise HTTPException(status_code=400, detail="Invalid language format. Use a two-letter code (e.g., 'en', 'fr').")

    # Insert into FAQ table
    new_faq = FAQ(id=id, question=faq.question, answer=faq.answer, language=faq.language)
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)
    flush_all_faqs()

    # Add the background task
    background_tasks.add_task(create_translations, db, new_faq.id, faq.question, faq.answer, faq.language)

    return new_faq


def create_translations(db: Session, new_faq_id: int, faq_question: str, faq_answer: str, faq_language: str):
    # Insert translations into FAQTranslation table
    for lang in DEFAULT_LANGUAGES:
        if lang != faq_language:
            # Translate the question and answer directly including HTML
            translated_question = translate_text(faq_question, lang)
            translated_answer = translate_text(faq_answer, lang)

            # Create and insert the translation entry
            faq_translation = FAQTranslation(
                faq_id=new_faq_id,
                language=lang,
                question=translated_question,
                answer=translated_answer
            )
            db.add(faq_translation)

    db.commit()

