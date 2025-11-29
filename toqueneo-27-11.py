import streamlit as st
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re

def get_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching URL: {e}")
        return None

def process_text(text):
    # Tokenize
    words = word_tokenize(text.lower())

    # Remove punctuation and non-alphabetic tokens
    words = [re.sub(r'[^a-z]', '', word) for word in words if word.isalpha()]

    # Remove stopwords
    stop_words = set(stopwords.words('spanish')) # Assuming Spanish content based on prompt
    words = [word for word in words if word not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Filter out empty strings that might result from cleaning
    words = [word for word in words if word]

    return words

st.set_page_config(layout="wide")
st.title("Análisis de Texto de Página Web")

url_input = st.text_input("Introduce la URL de la página web:", "")

if st.button("Analizar"):
    if url_input:
        with st.spinner("Cargando y procesando texto..."):
            raw_text = get_text_from_url(url_input)

            if raw_text:
                processed_words = process_text(raw_text)
                
                st.subheader("Texto Normalizado (fragmento):")
                st.code(" ".join(processed_words[:200]) + "...")

                st.subheader("Cantidad Total de Palabras:")
                st.write(f"El número total de palabras (después de tokenizar y normalizar) es: {len(processed_words)}")

                if processed_words:
                    word_counts = Counter(processed_words)
                    st.subheader("Palabras Más Frecuentes:")
                    
                    # Display top N frequent words
                    num_most_common = st.slider("Número de palabras más frecuentes a mostrar:", 5, 50, 10)
                    most_common_words = word_counts.most_common(num_most_common)

                    st.table(most_common_words)
                else:
                    st.warning("No se encontraron palabras después del procesamiento.")
            else:
                st.error("No se pudo obtener el texto de la URL proporcionada. Asegúrate de que la URL es válida y accesible.")
    else:
        st.warning("Por favor, introduce una URL para analizar.")

