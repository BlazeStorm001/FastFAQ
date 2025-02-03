from fastapi.testclient import TestClient
from app.main import app

from app.models.faq import FAQ, FAQTranslation

client = TestClient(app)

EXPECTED_TRANSLATIONS = {
    "bn": {
        "question": "আমার নাম কি?",
        "answer": "আমার নাম <b>জন ডো</b>"
    },
    "hi": {
        "question": "मेरा नाम क्या है?",
        "answer": "मेरा नाम <b>जॉन डो</b> है"
    }
}


def test_create_faq(db_session):
    try:
        # Prepare the data for the FAQ creation
        faq_data = {
            "question": "What is my name?",
            "answer": "My name is <b>John Doe</b>",
            "language": "en"
        }

        # Send POST request to create FAQ
        response = client.post("/api/faqs/", json=faq_data)
        # Assert the response status code
        assert response.status_code == 201
        assert response.json()["question"] == faq_data["question"]
        assert response.json()["answer"] == faq_data["answer"]

        # Check if the FAQ is inserted into the database
        faq_in_db = db_session.query(FAQ).filter(FAQ.question == faq_data["question"]).first()

        # Assert that the FAQ was inserted into the database
        assert faq_in_db is not None
        assert faq_in_db.question == faq_data["question"]
        assert faq_in_db.answer == faq_data["answer"]

        # Check if FAQTranslation entries are created
        faq_translations = db_session.query(FAQTranslation).filter(FAQTranslation.faq_id == faq_in_db.id).all()

        assert faq_translations is not None
        assert len(faq_translations) > 0  # Ensure at least one translation exists

        for translation in faq_translations:
            assert translation.language != faq_data["language"]  # Ensure translations are in different languages
            assert translation.question is not None
            assert translation.answer is not None

            # Validate translation correctness
            if translation.language in EXPECTED_TRANSLATIONS:
                expected = EXPECTED_TRANSLATIONS[translation.language]
                assert translation.question == expected["question"], f"Mismatch in {translation.language} question"
                assert translation.answer == expected["answer"], f"Mismatch in {translation.language} answer"

    finally:
        # Cleanup: Delete FAQTranslation entries first (to maintain foreign key constraints)
        for translation in faq_translations:
            db_session.delete(translation)

        # Cleanup: Delete FAQ entry
        db_session.delete(faq_in_db)
        db_session.commit()

        # Debugging
        print(f"Total records in the FAQ table: {len(db_session.query(FAQ).all())}")
        print(f"Total records in the FAQTranslation table: {len(db_session.query(FAQTranslation).all())}")

        # Ensure deletion
        faq_from_db = db_session.query(FAQ).filter(FAQ.question == faq_data["question"]).first()
        assert faq_from_db is None  # Entry should be deleted

        faq_translations_after_delete = db_session.query(FAQTranslation).filter(FAQTranslation.faq_id == faq_in_db.id).all()
        assert len(faq_translations_after_delete) == 0  # Ensure translations are deleted
