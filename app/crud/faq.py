from app.utils.lang_utils import translate_text, check_language_code
from sqlalchemy.orm import Session
from app.models.faq import FAQ, FAQTranslation
from app.config import DEFAULT_LANGUAGES
from app.schemas.faq import FAQCreate
from fastapi import HTTPException


def create_faq(db: Session, faq: FAQCreate):

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

