# app/crud/faq.py
from sqlalchemy.orm import Session
from app.models.faq import FAQ, FAQTranslation
from app.config import DEFAULT_LANGUAGES
from app.schemas.faq import FAQCreate

def create_faq(db: Session, faq: FAQCreate):
    # Insert into FAQ table
    new_faq = FAQ(question=faq.question, answer=faq.answer, language=faq.language)
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)

    # # Insert translations into FAQTranslation table
    # for lang in DEFAULT_LANGUAGES:
    #     if lang != faq.language:
    #         translated_question = translate(faq.question, lang)
    #         translated_answer = translate(faq.answer, lang)
    #         faq_translation = FAQTranslation(
    #             faq_id=new_faq.id, language=lang, question=translated_question, answer=translated_answer
    #         )
    #         db.add(faq_translation)
    
    db.commit()
    return new_faq

# def translate(text: str, language: str) -> str:
#     # Translation logic here (for now, just append language)
#     return f"{text} in {language}"
