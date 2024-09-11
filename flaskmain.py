import requests
from flask import Flask, request, jsonify
import os
import speech_recognition as sr
import time  # Pro měření latence
from main import OPENAI_API_KEY

app = Flask(__name__)

# Cesta k adresáři, kam budou ukládány nahrané soubory
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def send_to_openai_api(text):
    # URL OpenAI API
    url = 'https://api.openai.com/v1/chat/completions'

    # Headers with API key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(OPENAI_API_KEY)
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

    start_time = time.time()  # Start měření API latence
    print(f"OpenAI API response time: {start_time:.2f} seconds")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        api_time = time.time() - start_time  # Konec měření API latence
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices")[0].get("message").get("content").strip()
            print(f"OpenAI API response time: {api_time:.2f} seconds")
            return content
        else:
            return {'error': response.text}
    except requests.Timeout:
        return {'error': 'Request to OpenAI API timed out'}
    except requests.RequestException as e:
        return {'error': f'Request failed: {e}'}


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and (file.filename.endswith('.wav') or file.filename.endswith('.ogg')):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Použití speech_recognition pro převod řeči na text
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(file_path) as source:
                start_time = time.time()  # Start měření převodu řeči na text
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language='cs-CZ')
                transcription_time = time.time() - start_time  # Konec měření převodu řeči na text
                print(f"Speech recognition time: {transcription_time:.2f} seconds")

                response = send_to_openai_api(text)
                return jsonify({'message': 'File uploaded and processed successfully',
                                'file_path': file_path,
                                'transcription': text,
                                'response': response}), 200
        except sr.UnknownValueError:
            return jsonify({'response': 'Neslyšel jsem tě zkus to znovu.'}), 500
        except sr.RequestError as e:
            return jsonify({'error': f'Google Speech Recognition request failed; {e}'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
