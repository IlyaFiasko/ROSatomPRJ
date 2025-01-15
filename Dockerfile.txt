# 1. Используем базовый образ с Python
FROM python:3.10

# 2. Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    libsndfile-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Устанавливаем Whisper
RUN pip install openai-whisper

# 5. Копируем проект в контейнер
COPY . /app

# 6. Загружаем каждую модель по отдельности
RUN python -c "import whisper; whisper.load_model('tiny')"
RUN python -c "import whisper; whisper.load_model('base')"
RUN python -c "import whisper; whisper.load_model('small')"
RUN python -c "import whisper; whisper.load_model('medium')"

# 7. Открываем порт, на котором будет работать приложение Flask
EXPOSE 5000

# 8. Запускаем приложение
CMD ["python", "/app/app.py"]