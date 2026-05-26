import streamlit as st
import os
import time
import glob
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator


# ─────────────────────────────────────────────
# CONFIGURACIÓN VISUAL DE LA APP
# Solo modifica presentación general de la página.
# No cambia la lógica funcional de OCR, traducción ni audio.
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="OCR + Traductor de Voz",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ─────────────────────────────────────────────
# ESTILOS VISUALES
# Cambios estéticos:
# - Nueva tipografía.
# - Fondo verde menta claro.
# - Botones, selectores, checkboxes y uploader con estética más moderna.
# - Tarjetas visuales para organizar mejor la interfaz.
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(180deg, #effff8 0%, #dff8ee 100%) !important;
        color: #16382d !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #f7fffb !important;
        border-right: 1px solid #bfe8d8 !important;
        box-shadow: 4px 0 18px rgba(29, 111, 86, 0.08);
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0f513d !important;
        font-weight: 700 !important;
        letter-spacing: -0.2px !important;
    }

    [data-testid="stSidebar"] label {
        color: #215c48 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    /* Títulos */
    h1 {
        background: linear-gradient(135deg, #2fbf8f, #12805f);
        color: white !important;
        padding: 26px 32px;
        border-radius: 26px;
        box-shadow: 0 12px 28px rgba(18, 128, 95, 0.22);
        font-weight: 800 !important;
        letter-spacing: -0.8px !important;
        margin-bottom: 0.8rem !important;
    }

    h2, h3 {
        color: #0f513d !important;
        font-weight: 700 !important;
    }

    p, li, span, div, label {
        font-family: 'Poppins', sans-serif !important;
    }

    /* Subtítulos */
    .stMarkdown p {
        color: #315f50 !important;
        font-size: 0.96rem !important;
        line-height: 1.65 !important;
    }

    /* Inputs, text areas y selectores */
    textarea,
    input[type="text"],
    input[type="number"] {
        background-color: #ffffff !important;
        border: 1.5px solid #a9dfcb !important;
        border-radius: 16px !important;
        color: #16382d !important;
        font-size: 0.95rem !important;
        box-shadow: 0 6px 16px rgba(29, 111, 86, 0.08) !important;
        transition: all 0.2s ease !important;
    }

    textarea:focus,
    input[type="text"]:focus,
    input[type="number"]:focus {
        border-color: #2fbf8f !important;
        box-shadow: 0 0 0 4px rgba(47, 191, 143, 0.18) !important;
    }

    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1.5px solid #a9dfcb !important;
        border-radius: 16px !important;
        color: #16382d !important;
        box-shadow: 0 6px 16px rgba(29, 111, 86, 0.08) !important;
        transition: all 0.2s ease !important;
    }

    [data-baseweb="select"] > div:hover {
        border-color: #2fbf8f !important;
        box-shadow: 0 8px 18px rgba(29, 111, 86, 0.12) !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #ffffff !important;
        border: 1.5px dashed #7fd8b8 !important;
        border-radius: 20px !important;
        padding: 18px !important;
        box-shadow: 0 8px 18px rgba(29, 111, 86, 0.07) !important;
    }

    [data-testid="stFileUploader"] label {
        color: #0f513d !important;
        font-weight: 700 !important;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #37c99a, #12805f) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 1.3rem !important;
        box-shadow: 0 8px 18px rgba(18, 128, 95, 0.22) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2fbf8f, #0f6f53) !important;
        box-shadow: 0 12px 24px rgba(18, 128, 95, 0.30) !important;
        transform: translateY(-1px);
    }

    /* Checkboxes y radios */
    [data-testid="stCheckbox"],
    [data-testid="stRadio"] {
        background: #ffffff !important;
        border: 1px solid #c5eadb !important;
        border-radius: 18px !important;
        padding: 12px 14px !important;
        box-shadow: 0 5px 14px rgba(29, 111, 86, 0.06) !important;
    }

    div[role="radiogroup"] label {
        background: #f1fff8 !important;
        border: 1px solid #c5eadb !important;
        border-radius: 999px !important;
        padding: 6px 12px !important;
        margin: 4px 0 !important;
        transition: all 0.2s ease !important;
    }

    div[role="radiogroup"] label:hover {
        background: #dff8ee !important;
        border-color: #7fd8b8 !important;
    }

    /* Imágenes */
    [data-testid="stImage"] {
        border-radius: 22px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 24px rgba(29, 111, 86, 0.12) !important;
    }

    /* Alertas */
    [data-testid="stAlert"] {
        border-radius: 18px !important;
        border: 1px solid #bfe8d8 !important;
        box-shadow: 0 6px 16px rgba(29, 111, 86, 0.07) !important;
    }

    /* Audio */
    audio {
        width: 100%;
        border-radius: 18px;
    }

    /* Cards visuales */
    .mint-card {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid #c5eadb;
        border-radius: 24px;
        padding: 22px 24px;
        box-shadow: 0 10px 24px rgba(29, 111, 86, 0.08);
        margin-bottom: 18px;
    }

    .mint-card-title {
        color: #0f513d;
        font-size: 1.1rem;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .mint-help {
        color: #4d7868;
        font-size: 0.92rem;
        line-height: 1.55;
        margin-bottom: 0;
    }

    /* Texto OCR */
    .ocr-output {
        background: #ffffff;
        border: 1px solid #c5eadb;
        border-radius: 20px;
        padding: 18px;
        color: #16382d;
        font-size: 0.95rem;
        line-height: 1.7;
        box-shadow: 0 8px 18px rgba(29, 111, 86, 0.07);
        white-space: pre-wrap;
        min-height: 90px;
    }

    hr {
        border-color: #bfe8d8 !important;
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


# ─────────────────────────────────────────────
# ENCABEZADO
# Cambio estético:
# - Se mantiene el sentido del título.
# - Se mejora el texto visible para que sea más claro.
# ─────────────────────────────────────────────
st.title("🌿 Reconocimiento Óptico de Caracteres")
st.markdown("""
<div class="mint-card">
    <div class="mint-card-title">OCR, traducción y audio en una sola herramienta</div>
    <p class="mint-help">
        Elige una imagen desde la cámara o carga un archivo. La app extrae el texto,
        permite traducirlo y convertirlo en audio.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# Cambio estético y de orden visual:
# - Primero se agrupan los parámetros de imagen.
# - Luego los parámetros de traducción.
# - La lógica interna se conserva.
# ─────────────────────────────────────────────
with st.sidebar:
    st.subheader("⚙️ Configuración de imagen")
    filtro = st.radio("Filtro para imagen con cámara", ('Sí', 'No'))

    st.divider()

    st.subheader("🌎 Parámetros de traducción")

    try:
        os.mkdir("temp")
    except:
        pass

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
    elif out_lang == "Chinese":
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


# ─────────────────────────────────────────────
# CUERPO PRINCIPAL
# Cambio de orden visual:
# - Primero se muestran las opciones de fuente.
# - La cámara y el cargador quedan organizados en columnas.
# - No cambia el sentido de la aplicación.
# ─────────────────────────────────────────────
st.markdown("### 📥 Selecciona la fuente de la imagen")

col_fuente_1, col_fuente_2 = st.columns([1, 1], gap="large")

with col_fuente_1:
    st.markdown("""
    <div class="mint-card">
        <div class="mint-card-title">📷 Cámara</div>
        <p class="mint-help">Activa la cámara para tomar una foto directamente desde la app.</p>
    </div>
    """, unsafe_allow_html=True)

    cam_ = st.checkbox("Usar Cámara")

    if cam_:
        img_file_buffer = st.camera_input("Toma una Foto")
    else:
        img_file_buffer = None


with col_fuente_2:
    st.markdown("""
    <div class="mint-card">
        <div class="mint-card-title">🖼️ Archivo</div>
        <p class="mint-help">También puedes cargar una imagen en formato PNG o JPG.</p>
    </div>
    """, unsafe_allow_html=True)

    bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg"])


# ─────────────────────────────────────────────
# PROCESAMIENTO DE IMAGEN CARGADA
# Lógica original conservada.
# ─────────────────────────────────────────────
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='Imagen cargada.', use_container_width=True)

    # Guardar la imagen en el sistema de archivos
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())

    st.success(f"Imagen guardada como {uploaded_file.name}")

    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)


# ─────────────────────────────────────────────
# PROCESAMIENTO DE IMAGEN DESDE CÁMARA
# Lógica original conservada.
# ─────────────────────────────────────────────
if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)


# ─────────────────────────────────────────────
# TEXTO DETECTADO
# Cambio estético:
# - El texto OCR se muestra en una tarjeta visual.
# ─────────────────────────────────────────────
st.markdown("### 📝 Texto detectado")

st.markdown(
    f"""
    <div class="ocr-output">
        {text}
    </div>
    """,
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────
# CONVERSIÓN A AUDIO
# Cambio de orden visual:
# - El botón de conversión queda al final del flujo.
# - Se conserva la acción original del botón.
# ─────────────────────────────────────────────
st.markdown("### 🔊 Traducción y audio")

if st.button("Convertir texto a audio", use_container_width=True):
    result, output_text = text_to_speech(input_language, output_language, text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()

    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:
        st.markdown("## Texto de salida:")
        st.write(f" {output_text}")
