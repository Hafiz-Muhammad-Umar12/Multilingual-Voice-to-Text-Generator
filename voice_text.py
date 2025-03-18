import streamlit as st
import speech_recognition as sr
from googletrans import Translator

# 🎨 Streamlit UI
st.title("🎤 Multilingual Voice-to-Text Generator")

# ✅ Language Selection
languages = {
    "English": "en", "Urdu": "ur", "Hindi": "hi", "French": "fr", 
    "Spanish": "es", "German": "de", "Chinese": "zh-cn", "Arabic": "ar"
}

selected_lang = st.selectbox("Choose the language you will speak:", list(languages.keys()))

# 🎙️ Speech Recognition Function
def recognize_speech(lang_code):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Speak now... (Max 10 sec)")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            audio = recognizer.listen(source, timeout=10)  # Increased listening time
            text = recognizer.recognize_google(audio, language=lang_code)
            return text
        except sr.UnknownValueError:
            return "❌ Could not understand the speech."
        except sr.RequestError:
            return "❌ Speech service is unavailable."

# 📝 Start Voice Recording
if st.button("🎤 Start Recording"):
    st.success("Listening... Please speak.")
    recognized_text = recognize_speech(languages[selected_lang])

    if recognized_text and "❌" not in recognized_text:
        st.write("📝 **Generated Text (Original Language):**")
        st.write(f"💬 {recognized_text}")

        # 🔄 Automatically Translate to English
        translator = Translator()
        translated_text = translator.translate(recognized_text, src=languages[selected_lang], dest="en").text

        st.write("🌍 **Translated to English:**")
        st.write(f"💬 {translated_text}")
    else:
        st.error(recognized_text)
