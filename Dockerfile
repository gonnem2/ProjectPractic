FROM python:3.12.0

# Устанавливаем переменные окружения
ENV HOME=/home/fast \
    APP_HOME=/home/fast/app \
    PYTHONPATH="$PYTHONPATH:/home/fast" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p $APP_HOME \
 && groupadd -r fast \
 && useradd -r -g fast fast

# Устанавливаем необходимые утилиты
RUN apt-get update && apt-get install -y netcat-openbsd postgresql-client \
 && rm -rf /var/lib/apt/lists/*

WORKDIR $HOME

# Копируем файлы приложения
COPY app $APP_HOME
COPY alembic.ini .
COPY main.py .
COPY app/requirements.txt .

# Установка зависимостей и обновление pip
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && chown -R fast:fast .

# Копируем скрипт entrypoint
COPY entrypoint.sh $HOME/entrypoint.sh
RUN chmod +x $HOME/entrypoint.sh

# Меняем пользователя
USER fast

# Устанавливаем скрипт запуска
ENTRYPOINT ["bash", "/home/fast/entrypoint.sh"]
