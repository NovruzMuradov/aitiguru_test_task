"""
Основной файл приложения.
"""
from fastapi import FastAPI
from app.routers.orders import router as orders_router

app = FastAPI(
    title="Inventory Order Service",
    description="Сервис управления заказами и товарами",
    version="1.0.0",
)

app.include_router(orders_router, prefix="/api")
