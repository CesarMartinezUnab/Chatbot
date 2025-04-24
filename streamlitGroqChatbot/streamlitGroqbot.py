import streamlit as st
import pandas as pd
import time
from groq import Groq
from typing import Generator
from PIL import Image
import google.generativeai as genai
from io import BytesIO  # Para manejar imágenes correctamente

# Configuración del chatbot con Groq
st.title("Groq Bot Mejorado con Análisis de Imágenes y Gemini")

client = Groq(
    api_key=st.secrets["gsk"]["ngroq_key"]
)

# Configuración de Google Gemini API
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Lista de modelos disponibles en Groq
modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# Función para generar respuestas del chatbot
def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Genera respuestas de chat en tiempo real."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Inicialización del historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Sidebar: selección de modelo y carga de archivos
parModelo = st.sidebar.selectbox('Modelos', options=modelos, index=0)

uploaded_file = st.sidebar.file_uploader(
    "Adjunta un archivo (TXT, PDF, Word, Excel, Imagen)", 
    type=["txt", "pdf", "docx", "xls", "xlsx", "png", "jpg", "jpeg"]
)

if uploaded_file:
    try:
        st.sidebar.success(f"Archivo adjuntado: {uploaded_file.name}")

        # Procesamiento de imágenes con Gemini
        if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            img = Image.open(BytesIO(uploaded_file.getvalue()))  # Convierte los bytes en imagen correctamente
            st.image(img, caption="Imagen subida", use_column_width=True)

            # Enviar la imagen a Gemini API para análisis
            model = genai.GenerativeModel("gemini-1.5-flash")  # Más rápido  
            response = model.generate_content([img])  # Enviar imagen correctamente

            # Mostrar la descripción generada por Gemini
            st.write("Descripción de la imagen:", response.text)

            # Permitir preguntas sobre la imagen
            prompt_img = st.text_input("Escribe una consulta sobre la imagen")
            if prompt_img:
                img_query_response = model.generate_content([img, prompt_img])  # Consulta sobre la imagen
                st.write("Respuesta sobre la imagen:", img_query_response.text)

    except Exception as e:
        st.sidebar.error(f"Error al procesar el archivo: {e}")

# Campo de entrada de texto para el chatbot
prompt = st.chat_input("¿Qué quieres saber?")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        chat_completion = client.chat.completions.create(
            model=parModelo,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True
        )

        with st.chat_message("assistant"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(e)
