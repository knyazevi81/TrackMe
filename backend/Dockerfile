FROM python:3.10.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Указываем, что контейнер слушает на порту 8000
EXPOSE 8000