"""
Модуль описывающий routers.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services.order_service import add_product_to_order
from app.models.database import OrderItem
from pydantic import BaseModel

router = APIRouter()


@router.post("/orders/add-product")
def add_product(order_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    """
    Добавление товара в заказ через сервис.
    Если товар уже есть - увеличить количество.
    Если товара нет в наличии - вернуть ошибку.
    """
    success = add_product_to_order(db, order_id, product_id, quantity)
    if not success:
        raise HTTPException(status_code=400, detail="Not enough product quantity in stock or invalid order/product IDs")
    return {"status": "success"}


class OrderItemUpdate(BaseModel):
    quantity: int


@router.get("/orders/{order_id}/items/{product_id}")
def get_order_item(order_id: int, product_id: int, db: Session = Depends(get_db)):
    """
    Получить товар в заказе по order_id и product_id
    """
    item = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.product_id == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {
        "order_id": item.order_id,
        "product_id": item.product_id,
        "quantity": item.quantity
    }


@router.delete("/orders/{order_id}/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(order_id: int, product_id: int, db: Session = Depends(get_db)):
    """
    Удалить товар из заказа
    """
    item = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.product_id == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")
    db.delete(item)
    db.commit()
    return None


@router.put("/orders/{order_id}/items/{product_id}")
def update_order_item(order_id: int, product_id: int, update: OrderItemUpdate, db: Session = Depends(get_db)):
    """
    Обновить количество товара в заказе
    """
    item = db.query(OrderItem).filter(
        OrderItem.order_id == order_id,
        OrderItem.product_id == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order item not found")

    if update.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    item.quantity = update.quantity
    db.commit()
    db.refresh(item)
    return {
        "order_id": item.order_id,
        "product_id": item.product_id,
        "quantity": item.quantity
    }
