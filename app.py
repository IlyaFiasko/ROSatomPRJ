from flask import Flask, request, render_template, redirect, url_for, send_file
import whisper
import os
from datetime import datetime
import webbrowser

# Определение базовой директории проекта
base_dir = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(base_dir, "uploads")
transcriptions_dir = os.path.join(base_dir, "transcriptions")

app = Flask(__name__)
available_models = ["tiny", "base", "small", "medium", "large"]  # Доступные модели Whisper
current_model_name = "base"
model = whisper.load_model(current_model_name)
history = []  # Список для хранения истории транскрипций

@app.route("/", methods=["GET", "POST"])
def index():
    global history, model, current_model_name
    transcription = ""

    if request.method == "POST":
        # Обработка выбора модели
        if "model" in request.form:
            selected_model = request.form["model"]
            if selected_model in available_models:
                current_model_name = selected_model
                model = whisper.load_model(current_model_name)  # Загружаем выбранную модель

        # Обработка загрузки файла
        if "file" in request.files:
            file = request.files["file"]
            if file.filename == "":
                return redirect(request.url)
            
            if file:
                # Сохраняем файл для обработки
                file_name, file_extension = os.path.splitext(file.filename)
                file_path = os.path.join(uploads_dir, f"{file_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}")
                file.save(file_path)
                
                # Обработка файла с помощью выбранной модели Whisper
                result = model.transcribe(file_path)
                transcription = result["text"]
                
                # Добавляем транскрипцию в историю
                txt_filename = f"transcription_{file_name}.txt"
                history.append({
                    "filename": file.filename,
                    "transcription": transcription,
                    "txt_file": txt_filename,
                    "model": current_model_name
                })
                
                # Сохраняем результат в .txt файл
                txt_file_path = os.path.join(transcriptions_dir, txt_filename)
                with open((txt_file_path), "w", encoding="utf-8") as f:
                    f.write(transcription)
                
                # Удаляем исходный аудиофайл после транскрибации
                os.remove(file_path)
    
    return render_template(
        "index.html",
        history=history,
        current_model_name=current_model_name,
        available_models=available_models,
        transcription=transcription
    )

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(transcriptions_dir, filename), as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    if not os.path.exists(transcriptions_dir):
        os.makedirs(transcriptions_dir)

    # Небольшая задержка перед открытием браузера
    webbrowser.open("http://127.0.0.1:5000/")

    # Запускаем сервер Flask
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)  # use_reloader=False предотвращает повторный запуск сервера