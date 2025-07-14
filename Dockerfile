FROM python:3.10-slim

# 1. Установка базовых зависимостей
RUN apt-get update && apt-get install -y \
  && rm -rf /var/lib/apt/lists/*

# 2. Копируем и устанавливаем Python-зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем исходный код
COPY . .

# 4. Запускаем игру
CMD ["python", "main.py"]