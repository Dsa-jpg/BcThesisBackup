import os
import requests
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import speech_recognition as sr
from config.settings import  OPENAI_API_KEY


# FastAPI instance
app = FastAPI()

# Cesta k adresáři pro nahrané soubory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def send_to_openai_api(text):
    # URL OpenAI API
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
        ]
    }

    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        api_time = time.time() - start_time
        print(f"OpenAI API response time: {api_time:.2f} seconds")
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices")[0].get("message").get("content").strip()
            return content
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.Timeout:
        raise HTTPException(status_code=408, detail="Request to OpenAI API timed out")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f'Request failed: {e}')

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

            response = send_to_openai_api(text)
            return JSONResponse(content={
                'message': 'File uploaded and processed successfully',
                'file_path': file_path,
                'transcription': text,
                'response': response
            })
    except sr.UnknownValueError:
        raise HTTPException(status_code=500, detail="Neslyšel jsem tě, zkus to znovu.")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Google Speech Recognition request failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
