import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import SessionLocal
from app.models.faq import FAQ

client = TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    """Creates a new database session for a test and ensures cleanup after the test."""
    session = SessionLocal()
    yield session  # Provide the session to the test
    session.rollback()  # Rollback any changes
    session.close()  # Close session


def test_create_faq(db_session):
    from pdb import set_trace
    set_trace()
    # Prepare the data for the FAQ creation
    faq_data = {
        "question": "What is Python?",
        "answer": "Python is a programming language.",
        "language": "en"
    }

    # Send POST request to create FAQ
    response = client.post("/faqs/", json=faq_data)

    # Assert the response status code
    assert response.status_code == 200
    assert response.json()["question"] == faq_data["question"]
    assert response.json()["answer"] == faq_data["answer"]

    # Check if the FAQ is actually inserted into the database
    faq_in_db = db_session.query(FAQ).filter(FAQ.question == faq_data["question"]).first()

   
    # Assert that the FAQ was inserted into the database
    assert faq_in_db is not None
    assert faq_in_db.question == faq_data["question"]
    assert faq_in_db.answer == faq_data["answer"]
    
    # After the test, the transaction will be rolled back, so no changes will persist in the database

    # Cleanup: Delete test entry
    db_session.delete(faq_in_db)
    db_session.commit()
     # Debugging
    print(f"Total records in the FAQ table: {len(db_session.query(FAQ).all())}")
    
    # Ensure deletion
    faq_from_db = db_session.query(FAQ).filter(FAQ.question == "What is FastAPI?").first()
    assert faq_from_db is None  # Entry should be deleted
