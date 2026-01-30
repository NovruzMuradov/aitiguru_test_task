"""
Главный файл FastAPI приложения
"""
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import orders_router

# Создание приложения FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    REST API сервис для управления заказами и номенклатурой.

    ## Основные возможности:

    * **Добавление товара в заказ** - метод `POST /api/v1/orders/add-item`
      - Проверка наличия товара на складе
      - Автоматическое увеличение количества при повторном добавлении
      - Обновление складских остатков

    * **Просмотр информации** - методы `GET`
      - Информация о заказе
      - Информация о товаре

    ## Технический стек:

    * FastAPI
    * PostgreSQL
    * SQLAlchemy
    * Pydantic
    * Docker
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(orders_router)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Корневой эндпоинт",
    tags=["Health"]
)
async def root():
    """
    Корневой эндпоинт для проверки работоспособности API
    """
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Проверка здоровья сервиса",
    tags=["Health"]
)
async def health_check():
    """
    Health check эндпоинт для мониторинга
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }


# Обработчик глобальных исключений
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Глобальный обработчик исключений"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Внутренняя ошибка сервера",
            "details": str(exc) if settings.DEBUG else None
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )