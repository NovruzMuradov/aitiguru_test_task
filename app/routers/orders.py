"""
Модуль содержит роутер FastAPI для работы с заказами,
в частности, для добавления товара в заказ через сервис.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services.order_service import add_product_to_order

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
