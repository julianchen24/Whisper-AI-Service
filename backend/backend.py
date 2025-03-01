# venv\Scripts\activate
# Run both frontend and backend
# http://localhost:7860/

import whisper
from fastapi import FastAPI, UploadFile, File
import os
import uvicorn
import aiofiles
from pathlib import Path


app = FastAPI()

model = whisper.load_model("tiny")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), language: str = "auto"):
    file_path = UPLOAD_DIR / file.filename

    async with aiofiles.open(file_path,"wb") as buffer:
        await buffer.write(await file.read())

    try:
        options = {}
        if language != "auto":
            options["language"] = language
        result = model.transcribe(str(file_path),**options)
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.remove(file_path)

    return {"transcription": result["text"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)