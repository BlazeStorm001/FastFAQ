import re
from app.dependencies import translate_client

def check_language_code(language_code: str) -> bool:
    """
    Check if the given language code is a valid two-letter ISO 639-1 code.
    """

    # Define a regex pattern for language codes (ISO 639-1)
    LANGUAGE_CODE_PATTERN = re.compile(r"^[a-z]{2}$")

    return bool(LANGUAGE_CODE_PATTERN.match(language_code))


def translate_text(text: str, target_language: str) -> str:
    """Translates the given HTML text into the target language using Google Cloud Translation API."""
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']
