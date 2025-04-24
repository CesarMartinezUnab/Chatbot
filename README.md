# 🤖 CHATBOT_V4

## 📜 Descripción
Chatbot basado en inteligencia artificial con integración de **Groq** y **Gemini AI**, permitiendo análisis de imágenes y generación de respuestas interactivas.

## 🚀 Instalación

### 🔹 1. Clonar el repositorio
Desde la **carpeta de Descargas**, abre una terminal y ejecuta:
```bash
cd ~/Downloads  # En macOS/Linux
cd C:\Users\MyUser\Downloads  # En Windows

git clone https://github.com/CesarMartinezUnab/CHATBOT-4.0
cd CHATBOT-4.0
```

### 🔹 2. Crear y activar un entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate # Windows
source .venv/bin/activate # macOS/Linux
```

### 🔹 3. Instalar las dependencias del proyecto
```bash
# Ejecuta lo siguiente en la terminal:
pip install -r requirements.txt
```

### 🔹 4. Instalar google-generativeai individualmente
```bash
# Debido a que esta librería requiere una instalación separada, ejecuta:
pip install google-generativeai
```

### 🎯 Uso del chatbot
```bash
🔹 Acceder a la carpeta streamlitGroqChatbot
# Para ejecutar el chatbot desde la carpeta correcta:
cd streamlitGroqChatbot

🔹 Ejecutar el chatbot con Streamlit
streamlit run streamlitGroqbot.py
# Esto abrirá la aplicación en tu navegador y podrás empezar a chatear con la IA.
```

### ⚙️ Configuración adicional
```bash
# Si necesitas modificar las claves API de Groq o Gemini, edita el archivo secrets.toml:
[gsk]
ngroq_key = "TU-API-KEY-GROQ"

[gemini]
api_key = "TU-API-KEY-GEMINI"
```

### 🛠 Solución de problemas
```bash
🔹 Si pip install falla:
pip install --no-cache-dir -r requirements.txt

🔹 Si el entorno virtual tiene problemas, elimínalo y recréalo:
rm -rf .venv  # macOS/Linux
rmdir /s /q .venv  # Windows

python -m venv .venv
source .venv/bin/activate  # En Linux/macOS
.venv\Scripts\activate  # En Windows
pip install -r requirements.txt
pip install google-generativeai  # No olvides que esta instalación es por separada.
```