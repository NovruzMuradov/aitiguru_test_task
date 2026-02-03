"""
Модуль с настройками главного приложения.
"""
from fastapi import FastAPI
from app.routers.orders import router as orders_router

app = FastAPI(
    title="Inventory Order Service",
    description="Сервис управления заказами и товарами",
    version="1.0.0",
)

app.include_router(orders_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

