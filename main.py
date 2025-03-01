# venv\Scripts\activate

import whisper
from fastapi import FastAPI, UploadFile, File
import os
import uvicorn

app = FastAPI()

model = whisper.load_model("tiny")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), language: str = "auto"):
    file_path = f"temp_{file.filename}"
    with open(file_path,"wb") as buffer:
        buffer.write(await file.read())

    if language != "auto":
        result = model.transcribe(file_path,language=language)
    else: 
        result = model.transcribe(file_path)

    
    os.remove(file_path)

    return {"transcription": result["text"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)