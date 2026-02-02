import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, User, Item

TEST_DATABASE_URL = "postgresql://username:password@localhost:5432/test_db"


@pytest.fixture(scope="function")
def session():
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_create_user(session):
    user = User(username="testuser", email="test@example.com")
    session.add(user)
    session.commit()
    assert user.id is not None


def test_create_item(session):
    user = User(username="owner", email="owner@example.com")
    session.add(user)
    session.commit()

    item = Item(title="Test Item", owner_id=user.id)
    session.add(item)
    session.commit()

    assert item.id is not None
    assert item.owner == user
