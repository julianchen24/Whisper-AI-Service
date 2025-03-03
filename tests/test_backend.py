import pytest 
from httpx import AsyncClient
from fastapi.testclient import TestClient
import asyncio
import io

# To run tests, we must first run the backend 
# uvicorn backend.backend:app --host 127.0.0.1 --port 8000 --reload --log-level debug

@pytest.mark.asyncio
async def test_upload_audio():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        with open("sample.mp3", "rb") as audio_file:
            files = {"file": ("sample.wav",audio_file,"audio/mpeg")}
            response = await client.post("/transcribe/", files=files)

    assert response.status_code == 200
    assert "transcription" in response.json()
    assert response.json().get("transcription", None) is not None

@pytest.mark.asyncio
async def test_invalid_file():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        files = {"file": ("test.txt",b"Invalid data", "text/plain")}
        response = await client.post("/transcribe/", files=files)

    assert response.status_code == 500

@pytest.mark.asyncio
async def test_concurrent_requests():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        tasks = []
        with open("sample.mp3", "rb") as audio_file:
            file_data = audio_file.read() 
        # This is to simulate concurrent requests
        for i in range(5): 
            # IO Bytes is used to simulate a real file object rather than providing purely raw bytes
            files = {"file": (f"sample_{i}.mp3", io.BytesIO(file_data), "audio/mpeg")}  # Use file_data
            tasks.append(client.post("/transcribe/", files=files))  
        responses = await asyncio.gather(*tasks)  
    for response in responses:
        assert response.status_code == 200
        assert response.json().get("transcription", None) is not None


