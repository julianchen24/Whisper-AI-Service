# Whisper-AI 🎧🔊➞📝

Whisper-AI is an AI-powered speech-to-text transcription service using OpenAI's **Whisper** model. It allows users to upload **MP3** files and receive automatic transcriptions through a FastAPI backend and a **Gradio** web-based frontend.
![image](https://github.com/user-attachments/assets/b0a6bb81-e11c-4207-b296-68c975b059fe)

## 🚀 Features

- **MP3 Upload Support**: Accepts `.mp3` files for transcription.
- **Whisper AI Model**: Uses OpenAI’s **Whisper (Tiny model)** for accurate transcriptions.
- **FastAPI Backend**: Handles audio processing efficiently.
- **Gradio UI**: User-friendly web interface to upload files and view transcriptions.
- **Language Auto-detection**: Supports automatic language detection and manual selection (English, French, Spanish).
- **Concurrency Handling**: Limits to **5 simultaneous transcriptions** to prevent overload.
- **Robust Error Handling**: Gracefully handles incorrect file formats and server errors.
- **Automated Tests**: Uses **pytest** for unit and concurrency testing.

---

## 🏠 Installation

### 1️⃣ Clone the repository:

```sh
git clone https://github.com/julianchen24/Whisper-AI-Service.git
cd Whisper-AI-Service
```

### 2️⃣ Set up a Python virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On MacOS/Linux
venv\Scripts\activate      # On Windows
```

### 3️⃣ Install dependencies:

```sh
pip install -r requirements.txt
```

---

## ⚙️ Running the Service

### 🖥️ Start the Backend:

```sh
cd backend
uvicorn backend:app --host 127.0.0.1 --port 8000 --reload --log-level debug
```

- Runs the FastAPI server on **[http://127.0.0.1:8000](http://127.0.0.1:8000)**
- Exposes an API endpoint: **`/transcribe/`**

### 🌍 Start the Frontend:

```sh
cd frontend
python stt.py
```

- Opens a Gradio web interface at **[http://127.0.0.1:7860](http://127.0.0.1:7860)**
- Allows users to upload MP3 files and view transcriptions.

---

## 🎯 API Usage

### **Transcription Endpoint**

#### **POST** `/transcribe/`

Uploads an audio file and returns the transcribed text.

**Request:**

```sh
curl -X 'POST' 'http://127.0.0.1:8000/transcribe/' \
  -F 'file=@sample.mp3' \
  -F 'language=auto'
```

**Response:**

```json
{
  "transcription": "Hello, this is a sample transcription."
}
```

---

## 🛠️ Running Tests

To validate the API, run:

```sh
cd tests
pytest test_backend.py
```

Includes:

- **Audio upload test**
- **Invalid file type test**
- **Concurrency test (simulating multiple requests)**

---

## 🏆 Contributing

All contributions welcome.

---

## 📝 License

This project is licensed under the **MIT License**.

---

