import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database import Base, User, Item, Product, OrderItem

TEST_DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/inventory_db"


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

def test_create_product(session):
    product = Product(name="Test Product", description="Desc", quantity=10, price=100)
    session.add(product)
    session.commit()
    assert product.id is not None
    assert product.name == "Test Product"
    assert product.quantity == 10
    assert product.price == 100

def test_create_order_item(session):
    product = Product(name="Test Product", description="Desc", quantity=10, price=100)
    session.add(product)
    session.commit()

    # Создадим фиктивный order_id (требуется для ForeignKey)
    order_id = 1

    order_item = OrderItem(order_id=order_id, product_id=product.id, quantity=5)
    session.add(order_item)
    session.commit()

    assert order_item.id is not None
    assert order_item.product == product
    assert order_item.quantity == 5
    assert order_item.order_id == order_id