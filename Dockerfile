
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей и poetry
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Копируем файлы проекта
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости через poetry в режиме production
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
