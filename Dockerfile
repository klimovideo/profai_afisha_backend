# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Экспортируем порт, на котором будет работать FastAPI
EXPOSE 8001

# Команда запуска uvicorn с указанием модуля и хоста/порта из настроек
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
