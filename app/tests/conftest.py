import pytest
from app.database.session import SessionLocal

@pytest.fixture(scope="module")
def db_session():
    """Creates a new database session for a test and ensures cleanup after the test."""
    session = SessionLocal()
    yield session  # Provide the session to the test
    session.rollback()  # Rollback any changes
    session.close()  # Close session
