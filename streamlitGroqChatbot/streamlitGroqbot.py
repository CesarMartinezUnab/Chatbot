import streamlit as st
import pandas as pd
import time
from groq import Groq
from typing import Generator

st.title("Groq Bot")

# Declaramos el cliente de Groq
client = Groq(
    api_key=st.secrets["gsk"]["ngroq_key"]  # Con "gsk" cargamos la API key de la carpeta .streamlit/secrets.toml
)

# Lista de modelos para elegir
modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Genera respuestas de chat a partir de la información de completado de chat, mostrando caracter por caracter."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# Inicializamos el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Muestra mensajes de chat desde la historia en la aplicación cada vez que la aplicación se ejecuta
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Mostramos la lista de modelos en el sidebar
parModelo = st.sidebar.selectbox('Modelos', options=modelos, index=0)

# Funcionalidad de adjuntar documentos
uploaded_file = st.sidebar.file_uploader(
    "Adjunta tu archivo (TXT, PDF, Word, Excel)", 
    type=["txt", "pdf", "docx", "xls", "xlsx"]
)

if uploaded_file:
    try:
        st.sidebar.success(f"Archivo adjuntado: {uploaded_file.name}")
        
        # Procesar archivos de texto
        if uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")
            st.text_area("Contenido del archivo", content, height=200)

        # Procesar archivos de Excel
        elif uploaded_file.type in ["application/vnd.ms-excel", 
                                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
            df = pd.read_excel(uploaded_file)  # Leer el archivo Excel con pandas
            st.dataframe(df.head())  # Mostrar las primeras filas del archivo como tabla

        # Procesar archivos PDF
        elif uploaded_file.type == "application/pdf":
            st.info("Procesamiento de PDF aún no implementado.")

        # Procesar documentos Word
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            st.info("Procesamiento de documentos Word aún no implementado.")

    except Exception as e:
        st.sidebar.error(f"Error al procesar el archivo: {e}")

# Campo para el prompt del usuario
prompt = st.chat_input("Qué quieres saber?")

if prompt:
    # Mostrar mensaje de usuario en el contenedor de mensajes de chat
    st.chat_message("user").markdown(prompt)
    # Agregar mensaje de usuario al historial de chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        chat_completion = client.chat.completions.create(
            model=parModelo,
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],  # Entregamos el historial de los mensajes para que el modelo tenga algo de memoria
            stream=True
        )
        # Mostrar respuesta del asistente en el contenedor de mensajes de chat
        with st.chat_message("assistant"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            # Usamos st.write_stream para simular escritura
            full_response = st.write_stream(chat_responses_generator)
        # Agregar respuesta de asistente al historial de chat
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:  # Informamos si hay un error
        st.error(e)
