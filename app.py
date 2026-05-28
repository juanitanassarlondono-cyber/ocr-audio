import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

st.set_page_config(
    page_title="OCR Studio | Texto a Audio",
    page_icon="🔎",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top left, #102A43 0%, #07111F 40%, #020617 100%);
    color: #EAF6FF;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061728 0%, #020617 100%);
    border-right: 1px solid rgba(0, 217, 255, 0.18);
}

section[data-testid="stSidebar"] * {
    color: #EAF6FF;
}

.hero-card {
    padding: 2.4rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(0,153,255,.22), rgba(0,217,255,.08));
    border: 1px solid rgba(0,217,255,.28);
    box-shadow: 0 24px 80px rgba(0,153,255,.16);
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: .5rem;
    color: #FFFFFF;
}

.hero-subtitle {
    font-size: 1.1rem;
    color: #B8D7EA;
    line-height: 1.7;
    max-width: 780px;
}

.section-card {
    padding: 1.5rem;
    border-radius: 24px;
    background: rgba(8, 24, 42, 0.82);
    border: 1px solid rgba(0,217,255,.16);
    box-shadow: 0 18px 60px rgba(0,0,0,.24);
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #00D9FF;
    margin-bottom: .5rem;
}

.helper-text {
    color: #A9C4D8;
    font-size: .96rem;
    line-height: 1.6;
}

.stButton > button {
    width: 100%;
    border-radius: 16px;
    border: 1px solid rgba(0,217,255,.35);
    background: linear-gradient(135deg, #00D9FF, #0099FF);
    color: #020617;
    font-weight: 800;
    padding: .85rem 1rem;
    transition: all .25s ease;
    box-shadow: 0 12px 30px rgba(0,153,255,.28);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 45px rgba(0,217,255,.35);
    border-color: #8BE9FF;
}

div[data-testid="stFileUploader"] {
    border: 1px dashed rgba(0,217,255,.35);
    border-radius: 20px;
    padding: 1rem;
    background: rgba(0,153,255,.06);
}

div[data-testid="stCameraInput"] {
    border-radius: 20px;
    overflow: hidden;
}

.stRadio, .stSelectbox, .stCheckbox {
    background: rgba(255,255,255,.03);
    padding: .75rem;
    border-radius: 16px;
    border: 1px solid rgba(0,217,255,.10);
}

.output-box {
    padding: 1.25rem;
    border-radius: 20px;
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(0,217,255,.14);
    color: #EAF6FF;
    min-height: 120px;
    white-space: pre-wrap;
}

hr {
    border: none;
    height: 1px;
    background: rgba(0,217,255,.15);
    margin: 1.5rem 0;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2.1rem;
    }
    .hero-card {
        padding: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)


text = " "


def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text


def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)


remove_files(7)

try:
    os.mkdir("temp")
except:
    pass


st.markdown("""
<div class="hero-card">
    <div class="hero-title">OCR Studio</div>
    <div class="hero-subtitle">
        Reconocimiento óptico de caracteres, traducción y conversión de texto a audio en una interfaz moderna,
        limpia y optimizada para lectura.
    </div>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("### ⚙️ Panel de control")
    st.markdown("---")

    st.markdown("#### 📷 Procesamiento para cámara")
    filtro = st.radio("Filtro para imagen con cámara", ('Sí', 'No'))

    st.markdown("---")
    st.markdown("#### 🌐 Parámetros de traducción")

    translator = Translator()

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )

    if in_lang == "Ingles":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "koreano":
        input_language = "ko"
    elif in_lang == "Mandarin":
        input_language = "zh-cn"
    elif in_lang == "Japones":
        input_language = "ja"

    out_lang = st.selectbox(
        "Seleccione el lenguaje de salida",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )

    if out_lang == "Ingles":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "koreano":
        output_language = "ko"
    elif out_lang == "Mandarin":
        output_language = "zh-cn"
    elif out_lang == "Japones":
        output_language = "ja"

    english_accent = st.selectbox(
        "Seleccione el acento",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )

    if english_accent == "Default":
        tld = "com"
    elif english_accent == "India":
        tld = "co.in"
    elif english_accent == "United Kingdom":
        tld = "co.uk"
    elif english_accent == "United States":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Ireland":
        tld = "ie"
    elif english_accent == "South Africa":
        tld = "co.za"

    display_output_text = st.checkbox("Mostrar texto traducido")


left_col, right_col = st.columns([1.05, 0.95], gap="large")

with left_col:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">📥 Fuente de imagen</div>
        <div class="helper-text">
            Elige si quieres tomar una imagen desde la cámara o cargar una imagen desde tu computador.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cam_ = st.checkbox("Usar Cámara")

    if cam_:
        img_file_buffer = st.camera_input("Toma una foto")
    else:
        img_file_buffer = None

    bg_image = st.file_uploader("Cargar imagen:", type=["png", "jpg"])

    if bg_image is not None:
        uploaded_file = bg_image
        st.image(uploaded_file, caption='Imagen cargada.', use_container_width=True)

        with open(uploaded_file.name, 'wb') as f:
            f.write(uploaded_file.read())

        st.success(f"Imagen guardada como {uploaded_file.name}")

        img_cv = cv2.imread(f'{uploaded_file.name}')
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if filtro == 'Con Filtro':
            cv2_img = cv2.bitwise_not(cv2_img)
        else:
            cv2_img = cv2_img

        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)


with right_col:
    st.markdown("""
    <div class="section-card">
        <div class="section-title">📝 Texto reconocido</div>
        <div class="helper-text">
            Aquí aparecerá el texto extraído desde la imagen cargada o capturada con cámara.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="output-box">{text}</div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Convertir texto a audio"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()

        st.markdown("### 🎧 Tu audio")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("### 🌐 Texto de salida")
            st.write(f"{output_text}")
