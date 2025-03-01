from collections.abc import AsyncGenerator
from pathlib import Path

import gradio as gr
import httpx
from httpx_sse import aconnect_sse
import requests
# from speaches.config import Config
# from speaches.ui.utils import http_client_from_gradio_req, openai_client_from_gradio_req

# TRANSCRIPTION_ENDPOINT = "/v1/audio/transcriptions"
# TRANSLATION_ENDPOINT = "/v1/audio/translations"

WHISPER_API_URL = "http://127.0.0.1:8000/transcribe/"

def transcribe_audio(file_path, language="auto"):
    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}
        data = {"language": language}
        response = requests.post(WHISPER_API_URL,files=files,data=data)

    if response.status_code == 200:
        return response.json().get("transcription", "Error: No transcription found")

    else:
        return f"Error: {response.text}"
    

def create_stt_tab():
    with gr.Blocks() as demo:
        gr.Markdown("# AI Whisper Service")
        gr.Markdown("Upload an audio file and get an automatic transcription.")

        with gr.Row():
            audio = gr.Audio(type="filepath", label="Upload an Audio File")
            language_dropdown = gr.Dropdown(["auto","en","fr","es"], label="Language", value="auto")
        
        transcribe_button = gr.Button("Transcribe")
        output_text = gr.Textbox(label = "Transcription Output")

        transcribe_button.click(transcribe_audio, [audio,language_dropdown], output_text)
    
    return demo

if __name__ == "__main__":
    app = create_stt_tab()
    app.launch(server_name="0.0.0.0", server_port=7860)
        




