# venv\Scripts\activate
# Run both frontend and backend
# http://localhost:7860/

# To run speaches:
# cd speaches
# docker-compose up --build


import whisper
from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import uvicorn
import aiofiles
import asyncio
import logging
from pathlib import Path


app = FastAPI()

model = whisper.load_model("tiny")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# This is to limit concurrent requests to prevent overload, in this case limit to 5 concurrent transcription
semaphore = asyncio.Semaphore(5)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), language: str = "auto"):
    async with semaphore:
        file_path = UPLOAD_DIR / file.filename

        try:
            async with aiofiles.open(file_path,"wb") as buffer:
                await buffer.write(await file.read())

            options = {}
            if language != "auto":
                options["language"] = language
            result = model.transcribe(str(file_path),**options)

        except Exception as e:
            logger.error(f"Error transcribing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500,detail=f"Error processing file: {str(e)}")
        
        finally:
            os.remove(file_path)

        return {"transcription": result["text"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)