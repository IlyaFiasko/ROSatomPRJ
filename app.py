import streamlit as st
import whisper
import os
from io import StringIO

model = whisper.load_model("small")

os.system("apt-get update")
os.system("apt-get install -y ffmpeg")

# Функция для транскрибации
def transcribe_audio(file):
    temp_file_path = "temp_audio.wav"
    with open(temp_file_path, "wb") as f:
        f.write(file.getbuffer())

    # Проверка существует ли файл перед трансгрибацией
    if os.path.exists(temp_file_path):
        result = model.transcribe(temp_file_path)
        return result["text"]
    else:
        st.error("Ошибка: файл не найден.")
        return None


# Создание текстового файла
def create_txt_file(text):
    txt_file = StringIO()
    txt_file.write(text)
    txt_file.seek(0)
    return txt_file


st.title("Транскрибатор аудио")

st.header("Загрузите аудиофайл для транскрибации:")

audio_file = st.file_uploader("Выберите аудиофайл", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())

    # Транскрибация аудиофайла
    result = model.transcribe("temp_audio.wav")
    transcribed_text = result["text"]

    # Показываем результат на странице
    st.subheader("Результат транскрибации:")
    st.write(transcribed_text)

    # Преобразуем текст в байты
    byte_data = transcribed_text.encode()

    # Кнопка для скачивания файла
    st.download_button(
        label="Скачать результат транскрибации в формате .txt",
        data=byte_data,
        file_name="transcription.txt",
        mime="text/plain"
    )
