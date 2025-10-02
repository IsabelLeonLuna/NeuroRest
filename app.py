import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="NeuroRest", page_icon="🧠", layout="centered")

# Cargar claves: en Cloud usa st.secrets; en local puede existir .env
load_dotenv()
API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
MODEL  = st.secrets.get("GROQ_MODEL") or os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant"

if not API_KEY:
    st.error("Falta GROQ_API_KEY en Settings → Secrets (o en .env para local).")
    st.stop()

# Inicializa el cliente pasando la clave directamente (no uses os.environ[...] = ...).
client = Groq(api_key=API_KEY) # Cliente para invocar la API de Groq

# ------------------ Hero / Descripción del producto ------------------
st.title("🧠 NeuroRest — Prevención de caídas en adultos mayores")
st.markdown(
    """
**NeuroRest** es un dispositivo de monitoreo continuo que **detecta y previene caídas** en adultos mayores.  
Está diseñado para integrarse en la rutina diaria y brindar **alertas tempranas** a familiares y cuidadores.

**Beneficios clave:**
- ⚡ Detección temprana de riesgo de caída (inestabilidad, cambios de marcha).
- 📲 Alertas en tiempo real a cuidadores y familiares.
- 🔒 Seguridad y privacidad de datos.
- 💤 Mejora de la confianza y autonomía del adulto mayor.
"""
)

# (Opcional) Imagen/logo
# st.image("neurorest_logo.png", width=180)

st.divider()

# ------------------ Sidebar con info útil ------------------
with st.sidebar:
    st.header("ℹ️ Sobre NeuroRest")
    st.write(
        "- Uso cómodo y discreto\n"
        "- Batería de larga duración\n"
        "- Panel web para cuidadores\n"
        "- Integración con apps de salud"
    )
    st.subheader("Preguntas frecuentes")
    st.markdown(
        """
**¿Cómo funciona?**  
El dispositivo utiliza señales fisiológicas,como el SPO2, en conjunto con sensores de movimiento para prevenir caídas nocturnas de adultos mayores. No utiliza aprendizaje automático.

**¿Ha tenido algún incoveniente?**
Puede comunicarnos los problemas que se presenten en cualquier momento, nosotros le brindaremos atención.

**¿Compatibilidad?**  
Android/iOS para la app de cuidadores.

**Cuánto cuesta?**  
El dispositivo cuesta 350 soles (PEN). Se vende solo en Perú.
"""
    )
    st.caption("¿Quieres una demo privada? Deja tu correo en el chat.")

# ------------------ System prompt específico del producto ------------------
SYSTEM_PROMPT = (
    "Eres el asistente oficial de NeuroRest. "
    "Explica claramente cómo el dispositivo previene caídas en adultos mayores únicamente que utiliza sensores fisiológicos y de movimiento ante agitaciones noctunas, sus beneficios, "
    "casos de uso y consideraciones de privacidad. Sé empático, conciso y honesto. "
    "Si el usuario pide temas clínicos o regulatorios, responde con rigor y aclara alcances. "
    "El dispositivo cuesta 350 soles (PEN), solo se vende en Perú por el momento."
    "Evita prometer curas. Ofrece opciones de contacto o demo cuando sea útil. En caso quieran reportar alguna falla, brindar nuestro correo: neuro-rest@gmail.com"
)

# ------------------ Estado de la conversación ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ------------------ Cabecera del chat ------------------
st.subheader("💬 Asesor virtual de NeuroRest")
st.caption("Pregunta sobre uso, beneficios, instalación, privacidad, costos, etc.")

# Render del historial (omitimos el system)
for msg in st.session_state.chat_history:
    if msg["role"] == "system":
        continue
    with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
        st.markdown(msg["content"])

# ------------------ Entrada del usuario ------------------
user_msg = st.chat_input("Escribe tu consulta… (ej. ¿Cómo avisa al cuidador si detecta riesgo?)")

if user_msg:
    # Mostrar y guardar mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # Llamada al modelo
    try:
        with st.chat_message("assistant"):
            with st.status("Pensando…", expanded=False):
                resp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.chat_history,
                    temperature=0.6,
                    max_tokens=600,
                )
            answer = resp.choices[0].message.content
            st.markdown(answer)

        # Guardar respuesta
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
    except Exception as e:

        st.error(f"Ocurrió un problema llamando a Groq: {e}")



