"""
Модуль содержит функцию для добавления товара в заказ с проверкой наличия на складе.
"""
from sqlalchemy.orm import Session
from app.models.database import Base
from app.models import Product, OrderItem

def add_product_to_order(db: Session, order_id: int, product_id: int, quantity: int) -> bool:
    """
    Добавляет товар в заказ.
    Если товар есть - увеличивает количество.
    Проверяет наличие товара на складе.
    Возвращает True при успехе, False при ошибке.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or product.quantity < quantity:
        return False
    order_item = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.product_id == product_id
    ).first()
    if order_item:
        order_item.quantity += quantity
    else:
        order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
        db.add(order_item)
    product.quantity -= quantity
    db.commit()
    return True
