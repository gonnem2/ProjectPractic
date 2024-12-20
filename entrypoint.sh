#!/bin/bash
set -e

# Ожидание доступности базы данных
until pg_isready -h db -U "$POSTGRES_USER"; do
  echo "Waiting for database..."
  sleep 2
done

# Выполнение миграций
alembic upgrade head


# Запуск FastAPI-приложения
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
