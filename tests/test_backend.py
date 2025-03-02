import pytest 

from fastapi.testclient import TestClient
from backend.backend import app

client = TestClient(app)

def test_upload_audio():
    with open("sample.mp3", "rb") as audio_file:
        files = {"file": ("sample.wav",audio_file,"audio/mpeg")}
        response = client.post("/transcribe/", files=files)

    assert response.status_code == 200
    assert "transcription" in response.json()
    assert response.json().get("transcription", None) is not None

def test_invalid_file():
    files = {"file": ("test.txt",b"Invalid data", "text/plain")}
    response = client.post("/transcribe/", files=files)

    assert response.status_code == 500

def test_concurrent_requests():
    responses = []
    for i in range(5):
        with open("sample.mp3","rb") as audio_file:
            files = {"file": ("sample.mp3", audio_file,"audio/mpeg")}
            response = client.post("/transcribe/",files=files)
            responses.append(response)
        
    
    for response in responses:
        assert response.status_code == 200
        assert response.json().get("transcription",None) is not None

