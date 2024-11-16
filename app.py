import streamlit as st
import whisper
import os
from io import StringIO

model = whisper.load_model("base")

os.system("apt-get update")
os.system("apt-get install -y ffmpeg")

# Функция для транскрибации
def transcribe_audio(file):
    # Временный файл
    with open("temp_audio.wav", "wb") as f:
        f.write(file.getbuffer())

    # Whisper
    result = model.transcribe("temp_audio.wav")
    return result["text"]


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
    st.write("Загружен файл:", audio_file.name)

    if st.button("Транскрибировать"):
        st.write("Транскрибируем... Это может занять несколько секунд.")
        transcript = transcribe_audio(audio_file)

        st.subheader("Результат транскрибации:")
        st.text_area("Текст", transcript, height=200)

        st.subheader("Скачайте текстовый файл:")
        txt_file = create_txt_file(transcript)
        st.download_button(
            label="Скачать .txt файл",
            data=txt_file,
            file_name="transcript.txt",
            mime="text/plain"
        )
