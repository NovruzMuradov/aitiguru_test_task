# Inventory Order Service

REST API сервис для управления номенклатурой, заказами и клиентами с поддержкой иерархических категорий товаров.

## 📋 Описание проекта

Проект разработан как тестовое задание и включает:
- Проектирование схемы реляционной БД с иерархией категорий
- REST API сервис для добавления товаров в заказы
- Контейнеризацию с помощью Docker
- Полное покрытие тестами


## 🗄 Схема базы данных

### ER-диаграмма

```
┌─────────────────┐
│   Categories    │
│─────────────────│
│ id (PK)         │
│ name            │
│ parent_id (FK)  │◄────┐
│ level           │     │
└─────────────────┘     │
         ▲              │
         │              │
         └──────────────┘
         
┌─────────────────┐         ┌─────────────────┐
│  Nomenclature   │         │     Clients     │
│─────────────────│         │─────────────────│
│ id (PK)         │         │ id (PK)         │
│ name            │         │ name            │
│ quantity        │         │ address         │
│ price           │         └─────────────────┘
│ category_id(FK) │                  │
└─────────────────┘                  │
         │                           │
         │                           ▼
         │                  ┌─────────────────┐
         │                  │     Orders      │
         │                  │─────────────────│
         │                  │ id (PK)         │
         │                  │ client_id (FK)  │
         │                  │ order_date      │
         │                  │ status          │
         │                  │ total_amount    │
         │                  └─────────────────┘
         │                           │
         │                           │
         ▼                           ▼
    ┌──────────────────────────────────┐
    │        Order_Items               │
    │──────────────────────────────────│
    │ id (PK)                          │
    │ order_id (FK)                    │
    │ nomenclature_id (FK)             │
    │ quantity                         │
    │ price_at_order                   │
    │ subtotal (computed)              │
    │ UNIQUE(order_id, nomenclature_id)│
    └──────────────────────────────────┘
```

## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git

### Установка и запуск

1. **Клонировать репозиторий**
```bash
git clone https://github.com/NovruzMuradov/aitiguru_test_task.git
cd inventory-order-service
```

2. **Создать файл .env**
```bash
cp .env.example .env
```

3. **Запустить с помощью Docker Compose**
```bash
docker-compose up --build
```

Приложение будет доступно по адресу:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- PostgreSQL: localhost:5432

### Запуск без Docker (локально)

1. **Создать виртуальное окружение**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. **Установить зависимости**
```bash
pip install poetry
poetry init
```

3. **Настроить PostgreSQL**
```bash
# Создать БД и пользователя
psql -U postgres
CREATE DATABASE inventory_db;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO user;
```

4. **Применить схему БД**
```bash
psql -U user -d inventory_db -f database/schema.sql
```

5. **Запустить приложение**
```bash
uvicorn app.main:app --reload
```

## 📡 API Endpoints

### Документация

После запуска сервиса доступны:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc


## 🧪 Тестирование

### Запуск тестов

```bash
# В контейнере
docker-compose exec app pytest tests/ -v

# Локально
pytest tests/ -v
```


## 🔧 Конфигурация

### Переменные окружения (.env)

```env
DATABASE_URL=postgresql+psycopg2://user:password@db:5432/inventory_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=inventory_db
```


### ✅ Готово! Приложение запущено и готово к работе.


