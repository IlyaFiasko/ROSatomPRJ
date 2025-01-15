# Speech Transcriber

**Speech Transcriber** — это локальное веб-приложение, которое использует [Whisper](https://github.com/openai/whisper) для автоматической транскрипции аудиофайлов в текст. Проект реализован на Python и запускается в Docker-контейнере.

## Возможности

- Загрузка аудиофайлов в разных форматах.
- Автоматическое преобразование речи в текст.
- Простая настройка и запуск через Docker.

---

## Как установить и запустить

### 1. Склонируйте репозиторий

git clone https://github.com/4pokodav/local-transcriber.git

cd local-transcriber

git checkout master

### 2. Постройте Docker-образ

docker build -t speech-transcriber .

### 3. Запустите контейнер

docker run -d -p 8080:5000 --name speech-transcriber speech-transcriber

### 4. Откройте приложение

Перейдите в браузере по адресу http://localhost:8080

---

## Использование

1. Откройте веб-приложение.
2. Загрузите аудиофайл, который нужно транскрибировать.
3. Подождите завершения обработки — текст появится на экране.
4. Скачайте результат, если нужно.

---

## Использование через Docker Hub

Если вы хотите скачать готовый образ, выполните:

docker pull artemka2005/speech-transcriber:latest

docker run -d -p 8080:5000 --name speech-transcriber artemka2005/speech-transcriber:latest
