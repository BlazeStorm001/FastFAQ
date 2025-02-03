import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.faq import FAQ, FAQTranslation
from pdb import set_trace

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_and_teardown(db_session):
    # Insert test data into FAQ table
    faq1 = FAQ(question="hello this is a question", answer="this is a demo answer", language="en")
    faq2 = FAQ(question="त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है", answer="<p>त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है</p>", language="hi")
    db_session.add(faq1)
    db_session.add(faq2)
    db_session.commit()

    # Insert test data into FAQTranslation table
    translation1 = FAQTranslation(question="नमस्ते यह एक सवाल है", answer="यह एक डेमो उत्तर है", language="hi", faq_id=faq1.id)
    translation2 = FAQTranslation(
        question="The quick brown fox jumps over the lazy dog",
        answer="<p>The quick brown fox jumps over the lazy dog</p>",
        language="en",
        faq_id=faq2.id
    )
    translation3 = FAQTranslation(question="হ্যালো এই একটি প্রশ্ন", answer="এটি একটি ডেমো উত্তর।", language="bn", faq_id=faq1.id)
    translation4 = FAQTranslation(
        question="দ্রুত বাদামী শিয়াল অলস কুকুরের উপর ঝাঁপিয়ে পড়ে",
        answer="<p>দ্রুত বাদামী শিয়াল অলস কুকুরের উপর ঝাঁপিয়ে পড়ে</p>",
        language="bn",
        faq_id=faq2.id
    )
    db_session.add(translation1)
    db_session.add(translation2)
    db_session.add(translation3)
    db_session.add(translation4)
    db_session.commit()

    yield faq1.id, faq2.id

    # Cleanup: Delete all entries from FAQTranslation and FAQ tables
    db_session.query(FAQTranslation).filter(
        (FAQTranslation.faq_id == faq1.id) | (FAQTranslation.faq_id == faq2.id)
    ).delete()
    db_session.query(FAQ).filter(
        (FAQ.id == faq1.id) | (FAQ.id == faq2.id)
    ).delete()
    db_session.commit()

def test_get_all_faqs_in_english(setup_and_teardown):
    response = client.get("/api/faqs/")
    assert response.status_code == 200
    faqs = response.json()
    assert any(faq["question"] == "hello this is a question" and faq["answer"] == "this is a demo answer" for faq in faqs)
    assert any(
        faq["question"] == "The quick brown fox jumps over the lazy dog"
        and faq["answer"] == "<p>The quick brown fox jumps over the lazy dog</p>"
        for faq in faqs
    )


def test_get_faq_by_id_in_english(setup_and_teardown):
    _, faq2_id = setup_and_teardown
    set_trace()
    response = client.get(f"/api/faqs/?id={faq2_id}")
    assert response.status_code == 200
    faq = response.json()
    assert faq[0]["question"] == "The quick brown fox jumps over the lazy dog"
    assert faq[0]["answer"] == "<p>The quick brown fox jumps over the lazy dog</p>"

def test_get_all_faqs_in_hindi(setup_and_teardown):
    response = client.get("/api/faqs/?lang=hi")
    assert response.status_code == 200
    faqs = response.json()
    assert any(
        faq["question"] == "त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है" and
        faq["answer"] == "<p>त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है</p>"
        for faq in faqs
    )
    assert any(faq["question"] == "नमस्ते यह एक सवाल है" and faq["answer"] == "यह एक डेमो उत्तर है" for faq in faqs)

def test_get_faq_by_id_in_hindi(setup_and_teardown):
    _, faq2_id = setup_and_teardown
    set_trace()
    response = client.get(f"/api/faqs/?id={faq2_id}&lang=hi")
    assert response.status_code == 200
    faq = response.json()
    assert faq[0]["question"] == "त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है"
    assert faq[0]["answer"] == "<p>त्वरित भूरी लोमड़ी आलसी कुत्ते के ऊपर से छलांग लगाती है</p>"
