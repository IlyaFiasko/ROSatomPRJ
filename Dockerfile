FROM python:3.12-slim

# Устанавливаем FFmpeg (необходим для обработки аудио в Whisper)
RUN apt-get update && apt-get install -y ffmpeg

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Шаг 6: Копируем все файлы вашего проекта в контейнер
COPY . /app/

# Открываем порт, который будет использоваться Streamlit (по умолчанию это 8501)
EXPOSE 8501

#  Запускаем приложение Streamlit
CMD ["streamlit", "run", "app.py"]