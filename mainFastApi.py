import os
import requests
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import speech_recognition as sr
import aiohttp

# FastAPI instance
app = FastAPI()

# Cesta k adresáři pro nahrané soubory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Načtení API klíče z prostředí


async def stream_openai_api(text):
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "Jsi humanoidní robot jménem NAO. Tvůj domov je v Českých Budějovicích, konkrétně na Jihočeské Univerzitě v koleji K3. Tvůj věk je 5 let, což pro robota jako jsi ty znamená, že jsi v plné síle svých schopností."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "stream": True  # Povolení streamování odpovědi
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=f"OpenAI API error: {resp.status}")
            
            async for chunk in resp.content.iter_chunked(1024):
                if chunk:
                    yield chunk.decode('utf-8')

# curl --location "http://127.0.0.1:8000/upload/" --form "file=@C:\Users\Filip\Downloads\recordPetr.wav"
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Validace formátu souboru
    if not (file.filename.endswith('.wav') or file.filename.endswith('.ogg')):
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Převod řeči na text pomocí SpeechRecognition
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            start_time = time.time()
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='cs-CZ')
            transcription_time = time.time() - start_time
            print(f"Speech recognition time: {transcription_time:.2f} seconds")

            # Streamování odpovědi z OpenAI API
            return StreamingResponse(stream_openai_api(text), media_type="text/plain")
    except sr.UnknownValueError:
        raise HTTPException(status_code=500, detail="Neslyšel jsem tě, zkus to znovu.")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Google Speech Recognition request failed: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
