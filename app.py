import streamlit as st
from transformers import pipeline
import io
from pdfminer.high_level import extract_text_to_fp
import time

# Titolo del sito
st.title("Riassumitore di Testi e PDF (Versione Online Gratuita con Avanzamento)")

# Modello IA
model_name = "pszemraj/led-large-book-summary"
summarizer = pipeline("summarization", model=model_name)

def riassumi(testo, percentuale):
    if not testo:
        return ""
    lunghezza_input = len(testo.split())
    max_lunghezza = int(lunghezza_input * (percentuale / 100.0)) + 100
    min_lunghezza = int(max_lunghezza * 0.5)
    with st.spinner("Elaborazione in corso..."):
        riassunto = summarizer(testo, min_length=min_lunghezza, max_length=max_lunghezza, no_repeat_ngram_size=3, encoder_no_repeat_ngram_size=3)[0]['summary_text']
    return riassunto

def estrai_testo_da_pdf(uploaded_file):
    try:
        bytes_data = uploaded_file.read()
        text_content = extract_text_to_fp(io.BytesIO(bytes_data))
        return text_content
    except Exception as e:
        st.error(f"Errore nel caricamento o lettura del PDF: {e}")
        return ""

# Area per caricare il PDF
uploaded_file = st.file_uploader("Carica un file PDF", type=["pdf"])

testo_da_riassumere = ""
if uploaded_file is not None:
    testo_da_riassumere = estrai_testo_da_pdf(uploaded_file)
else:
    testo_da_riassumere = st.text_area("Oppure incolla qui il testo da riassumere:", height=200)

# Scelta della percentuale
percentuale_riduzione = st.slider("Percentuale di riduzione desiderata:", 10, 80, 30)

# Bottone per riassumere
if st.button("Riassumi"):
    if testo_da_riassumere:
        st.subheader("Riassunto:")
        risultato_riassunto = riassumi(testo_da_riassumere, percentuale_riduzione)
        st.write(risultato_riassunto)
    else:
        st.warning("Inserisci del testo o carica un PDF.")