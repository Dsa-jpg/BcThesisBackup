from flask import Flask, Response, jsonify, request
from openai import OpenAI
import os
import speech_recognition as sr

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UPLOAD_FOLDER = 'app/uploads'
PROMPT = "Jsi humanoidní robot jménem NAO. Tvůj domov je v Českých Budějovicích, konkrétně na Jihočeské Univerzitě v koleji K3. Tvůj věk je 5 let, což pro robota jako jsi ty znamená, že jsi v plné síle svých schopností. Odpovídej stručně a maximalně do dvou vět."
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
client = OpenAI(api_key=OPENAI_API_KEY)
app = Flask(__name__)


@app.route('/response')
def get_response():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Kdo je prezident CR?"}
            ],
            stream=True,
            max_tokens=200
        )

        def generate_response():
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content 

        return Response(generate_response(), mimetype="text/event-stream")

    except Exception as e:
        return Response(f"An error occured {e}", status=500)


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

                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language='cs-CZ')
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": PROMPT},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=200,
                    stream=True
                )

                def generate_response():
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            yield chunk.choices[0].delta.content

                return Response(generate_response(), mimetype="text/event-stream")
        except sr.UnknownValueError:
            return jsonify({'response': 'Neslyšel jsem tě zkus to znovu.'}), 500
        except sr.RequestError as e:
            return jsonify({'error': f'Google Speech Recognition request failed; {e}'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
