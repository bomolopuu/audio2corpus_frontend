import streamlit as st
import requests

# Set page configuration
st.set_page_config(
    page_title="Audio2Transcription",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS for sound waves theme
soundwaves_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&display=swap');

/* Base styles */
.stApp {
    background: #000 !important;
    color: #fff;
}

/* Container styles */
.main-container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Title styles */
h1 {
    font-family: 'Syncopate', sans-serif !important;
    color: #fff !important;
    text-transform: uppercase;
    letter-spacing: 5px;
    text-align: center;
    font-size: 2.5rem !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 0 10px rgba(0, 255, 135, 0.5);
}

/* Subtitle styles */
.subtitle {
    font-family: 'Syncopate', sans-serif !important;
    color: rgba(255, 255, 255, 0.8) !important;
    text-align: center;
    font-size: 1.2rem !important;
    margin-bottom: 3rem !important;
    letter-spacing: 2px;
}

/* Audio visualizer */
@keyframes equalize {
    0% { height: 60px; }
    50% { height: 10px; }
    100% { height: 60px; }
}

.equalizer {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4px;
    height: 80px;
    margin: 2rem 0;
}

.bar {
    width: 4px;
    height: 60px;
    background: linear-gradient(45deg, #00ff87, #60efff);
    border-radius: 2px;
}

/* Generate bars with different animations */
.bar:nth-child(1) { animation: equalize 0.8s ease-in-out infinite; }
.bar:nth-child(2) { animation: equalize 0.9s ease-in-out infinite; }
.bar:nth-child(3) { animation: equalize 1.0s ease-in-out infinite; }
.bar:nth-child(4) { animation: equalize 1.1s ease-in-out infinite; }
.bar:nth-child(5) { animation: equalize 0.8s ease-in-out infinite; }
.bar:nth-child(6) { animation: equalize 0.9s ease-in-out infinite; }
.bar:nth-child(7) { animation: equalize 1.0s ease-in-out infinite; }
.bar:nth-child(8) { animation: equalize 1.1s ease-in-out infinite; }

/* File uploader styles */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 2px dashed rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

.uploadedFile {
    color: #00ff87 !important;
}

/* Button styles */
.stButton > button {
    width: 100%;
    background: transparent !important;
    border: 2px solid #00ff87 !important;
    color: #00ff87 !important;
    border-radius: 25px !important;
    padding: 0.8rem 2rem !important;
    font-family: 'Syncopate', sans-serif !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    transition: all 0.3s ease !important;
    margin-top: 1rem !important;
}

.stButton > button:hover {
    background: #00ff87 !important;
    color: #000 !important;
    box-shadow: 0 0 20px #00ff87;
}

/* Transcription box */
.transcription-box {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid #00ff87;
    border-radius: 10px;
    padding: 2rem;
    margin: 2rem 0;
    color: #fff;
    font-family: monospace;
    font-size: 1rem;
    line-height: 1.6;
    box-shadow: 0 0 20px rgba(0, 255, 135, 0.2);
}

/* Audio player */
audio {
    width: 100%;
    margin: 1rem 0;
    border-radius: 25px;
}

/* Footer */
.footer-text {
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.8rem;
    margin-top: 2rem;
    font-family: 'Syncopate', sans-serif;
}

/* Link styles */
a {
    color: #00ff87 !important;
    text-decoration: none;
    transition: all 0.3s ease;
}

a:hover {
    color: #60efff !important;
    text-shadow: 0 0 10px #60efff;
}

/* Loading spinner */
.stSpinner > div {
    border-top-color: #00ff87 !important;
    border-right-color: #60efff !important;
    border-bottom-color: #00ff87 !important;
    border-left-color: #60efff !important;
}

/* Hide Streamlit branding */
#MainMenu, footer {
    visibility: hidden;
}
</style>
"""

# Initialize session state
if 'is_transcribing' not in st.session_state:
    st.session_state.is_transcribing = False

# Add custom CSS
st.markdown(soundwaves_css, unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title and Subtitle
st.title("Audio2Transcription")
st.markdown('<p class="subtitle">This app transcribes speech to text</p>', unsafe_allow_html=True)

# Equalizer bars
equalizer_html = """
<div class="equalizer">
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
    <div class="bar"></div>
</div>
"""
st.markdown(equalizer_html, unsafe_allow_html=True)

# File uploader
audio_file = st.file_uploader("Upload your audio file", type=['wav', 'mp3', 'm4a'])

if audio_file:
    if st.button("Start Transcription"):
        st.session_state.is_transcribing = True

        with st.spinner('Transcribing...'):
            try:
                url = 'https://audio2corpus-184611756849.europe-west1.run.app/transcribe/'
                response = requests.post(url, files={'audio_file': audio_file})

                # Display transcription
                transcription = response.json()['transcription']
                st.markdown(f"""
                    <div class="transcription-box">
                        {transcription}
                    </div>
                """, unsafe_allow_html=True)

                # Display audio player
                st.audio(audio_file)

                # Show footer
                st.markdown("""
                    <div class="footer-text">
                        Powered by MMS Model |
                        <a href="https://ai.meta.com/blog/multilingual-model-speech-recognition/" target="_blank">
                        Meta AI</a> | Project by Tatiana Korol, Razif Haque, Akos Steger and Adam Ouayda with Le Wagon Teachers
                    </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error("Transcription failed. Please try again.")

            finally:
                st.session_state.is_transcribing = False

st.markdown('</div>', unsafe_allow_html=True)
