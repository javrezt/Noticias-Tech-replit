import os
import requests
import streamlit as st
from bs4 import BeautifulSoup

# Título y encabezados
st.title("Quest")
st.subheader("Mastering the Art of Prompt Engineering")
st.write("---")
st.header("Noticias tech")

query = st.text_input("¿Qué quieres saber hoy?")
url = st.text_input("Envíame la URL:")

if st.button("Buscar"):
    if query and url:
        # Realizar solicitud a la URL
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            body_content = soup.find("body").get_text(separator="\n", strip=True)

            # Configuración de la API de OpenAI
            #openai_api_key = os.environ["OPENAI_API_KEY"]
            headers = {
                "Authorization": "Bearer app-ETJWaNRdtsfadpSFTHzJcKZV",
                "Content-Type": "application/json" 
            }

            data = {
                "inputs": {
                    "query": query,
                    "url": url
                },
                "response_mode": "blocking",
                "user": "LS-08"
            }

            # Mostrar datos para depuración
            # st.write("Datos enviados a la API:", data)  
            # Mostrar encabezados para depuración
            # st.write("Encabezados:", headers)  

            try:
                base_url = "https://api.dify.ai/v1/workflows/run"  # Ruta completa según documentación de DIFY
                response = requests.post(base_url, json=data, headers=headers)
                response.raise_for_status()  # Levantar un error si la solicitud no fue exitosa
                result = response.json()

                # Mostrar la respuesta completa de la API para depuración
                # st.write("Respuesta completa de la API:", result)

                # Verificar si la respuesta contiene el contenido esperado
                if 'outputs' in result['data'] and 'text' in result['data']['outputs']:
                    # Mostrar el resultado en markdown
                    st.markdown(f"**Resultado:**\n\n{result['data']['outputs']['text']}")
                else:
                    st.error("La respuesta de la API no contiene el contenido esperado.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error en la solicitud: {e}")
        else:
            st.error(f"Error al acceder a la URL: {response.status_code}")
    else:
        st.warning("Por favor, ingresa una consulta y una URL.")
