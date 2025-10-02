# NeuroRest – Asistente de producto 

Asistente conversacional para NeuroRest, un dispositivo de prevención de caídas en adultos mayores.
Incluye una sección de presentación y un chat que responde preguntas sobre uso, precio, conexión, carga y soporte técnico.
Las respuestas “oficiales” se gestionan desde faqs.yaml (sin tocar el código).

Demo local: python -m streamlit run app.py

✨ Características

Hero con beneficios de NeuroRest.

Chat con historial y tono de asesor del producto.

FAQs configurables en faqs.yaml con placeholders (precio, contacto, URL).

Fallback a LLM (Groq) para preguntas abiertas.

Listo para desplegar en Streamlit Community Cloud
