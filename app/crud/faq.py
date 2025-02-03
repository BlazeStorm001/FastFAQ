from google.cloud import translate_v2 as translate
from sqlalchemy.orm import Session
from app.models.faq import FAQ, FAQTranslation
from app.config import DEFAULT_LANGUAGES
from app.schemas.faq import FAQCreate

# Initialize the Google Translate API client
translate_client = translate.Client()

def create_faq(db: Session, faq: FAQCreate):
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

def translate_text(text: str, target_language: str) -> str:
    """Translates the given HTML text into the target language using Google Cloud Translation API."""
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText'] 
