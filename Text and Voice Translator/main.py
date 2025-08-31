import streamlit as st
from googletrans import Translator
import speech_recognition as sr

# Translator init
translator = Translator()

# Page config
st.set_page_config(page_title="Text & Voice Translator", layout="centered")
st.title("Text & Voice Translator")

# Session state init
if "text_translation" not in st.session_state:
    st.session_state.text_translation = ""
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""
if "voice_translation" not in st.session_state:
    st.session_state.voice_translation = ""

# Language selection
lang_options = {
    "Hindi": "hi",
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Russian": "ru",
    "Arabic": "ar"
}

st.subheader("please Select Languages")
source_lang = st.selectbox("Source Language", list(lang_options.keys()))
target_lang = st.selectbox("Target Language", list(lang_options.keys()))

# ---------------- TEXT TRANSLATION ----------------
st.markdown("---")
st.header("Text Translator")

text_input = st.text_area("Enter text here:", height=100)

if st.button("Translate Text"):
    if text_input.strip() != "":
        result = translator.translate(text_input, src=lang_options[source_lang], dest=lang_options[target_lang])
        st.session_state.text_translation = result.text
    else:
        st.warning(" Please enter some text before translating.")

st.text_area("Text Translation Result:", value=st.session_state.text_translation, height=100, disabled=True)

# ---------------- VOICE TRANSLATION ----------------
st.markdown("---")
st.header("Voice Translator")

# Speak button
if st.button("Speak Now..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak")
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        voice_text = recognizer.recognize_google(audio, language=lang_options[source_lang])
        st.session_state.voice_input = voice_text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand the audio ")
    except sr.RequestError:
        st.error("Speech Recognition service error ")

# Show spoken text in textbox
st.text_area("Spoken Text:", value=st.session_state.voice_input, height=100)

# Translate button for voice input
if st.button("Translate Spoken Text"):
    if st.session_state.voice_input.strip() != "":
        result = translator.translate(st.session_state.voice_input, src=lang_options[source_lang], dest=lang_options[target_lang])
        st.session_state.voice_translation = result.text
    else:
        st.warning(" No spoken text found. Please click Speak Now first.")

st.text_area("Voice Translation Result:", value=st.session_state.voice_translation, height=100, disabled=True)
