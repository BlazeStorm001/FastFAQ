import pytest
from app.database.session import SessionLocal
from app.models.faq import FAQ

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for a test and ensures cleanup after the test."""
    session = SessionLocal()
    yield session  # Provide the session to the test
    session.rollback()  # Rollback any changes
    session.close()  # Close session

def test_create_faq(db_session):
    """Test FAQ creation and ensure cleanup after test"""
    faq = FAQ(question="What is FastAPI?", answer="A modern web framework for APIs.", language="en")

    db_session.add(faq)
    db_session.commit()

    # Fetch FAQ
    faq_from_db = db_session.query(FAQ).filter(FAQ.question == "What is FastAPI?").first()
    assert faq_from_db is not None
    assert faq_from_db.question == "What is FastAPI?"

    # Cleanup: Delete test entry
    db_session.delete(faq_from_db)
    db_session.commit()

    # Ensure deletion
    faq_from_db = db_session.query(FAQ).filter(FAQ.question == "What is FastAPI?").first()
    assert faq_from_db is None  # Entry should be deleted
