FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Делаем рабочей директорией корень проекта
WORKDIR /app

# Добавляем корневую директорию в PYTHONPATH
ENV PYTHONPATH=/app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

# Запуск бота
CMD ["python", "tg_bot/bot.py"]
