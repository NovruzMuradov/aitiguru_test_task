# Inventory Order Service

REST API сервис для управления номенклатурой, заказами и клиентами с поддержкой иерархических категорий товаров.

## 📋 Описание проекта

Проект разработан как тестовое задание и включает:
- Проектирование схемы реляционной БД с иерархией категорий
- SQL запросы для анализа данных и построения отчетов
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

## 📊 SQL Запросы

### 2.1. Сумма товаров по клиентам

```sql
SELECT 
    c.name AS client_name,
    COALESCE(SUM(oi.subtotal), 0) AS total_amount
FROM clients c
LEFT JOIN orders o ON c.id = o.client_id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.id, c.name
ORDER BY total_amount DESC;
```

### 2.2. Количество дочерних категорий первого уровня

```sql
SELECT 
    c.id AS category_id,
    c.name AS category_name,
    c.level AS category_level,
    COUNT(child.id) AS first_level_children_count
FROM categories c
LEFT JOIN categories child ON c.id = child.parent_id
GROUP BY c.id, c.name, c.level
ORDER BY c.level, c.id;
```


## 🚀 Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- Git

### Установка и запуск

1. **Клонировать репозиторий**
```bash
git clone https://github.com/YOUR_USERNAME/inventory-order-service.git
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
psql -U user -d inventory_db -f database/seed_data.sql
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

### Покрытие тестов

Тесты включают проверку:
- ✅ Успешного добавления товара
- ✅ Увеличения количества существующего товара
- ✅ Ошибки при недостатке товара
- ✅ Ошибки при несуществующем заказе
- ✅ Ошибки при несуществующем товаре
- ✅ Валидации входных данных
- ✅ Получения информации о заказе и товаре



## 🔧 Конфигурация

### Переменные окружения (.env)

```env
DATABASE_URL=postgresql://user:password@db:5432/inventory_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=inventory_db
```

### Настройки приложения (app/config.py)

```python
class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Inventory Order Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
```

## 📤 Загрузка на GitHub

### Пошаговая инструкция

1. **Создать репозиторий на GitHub**
   - Перейти на https://github.com/new
   - Название: `inventory-order-service`
   - Описание: `REST API сервис для управления заказами и номенклатурой`
   - Не инициализировать с README

2. **Инициализировать Git локально**
```bash
cd inventory-order-service
git init
git add .
git commit -m "Initial commit: Inventory Order Service

- Схема БД с иерархией категорий
- SQL запросы для анализа данных
- REST API на FastAPI
- Docker контейнеризация
- Полное покрытие тестами"
```

3. **Подключить удалённый репозиторий**
```bash
git remote add origin https://github.com/YOUR_USERNAME/inventory-order-service.git
git branch -M main
git push -u origin main
```
