import urllib
import urllib2
import mimetypes

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.file_path = '/home/nao/recordings/microphones/record.wav'
        self.api_url = 'http://172.20.10.4:5000/upload'  # Změň na URL tvého Flask server
        self.tts = ALProxy('ALTextToSpeech')

    def onLoad(self):
        # Iniciální kód
        pass

    def onUnload(self):
        # Úklidový kód
        pass

    def onInput_onStart(self):
        self.send_file()  # Volání metody pro odeslání souboru
        pass

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()

    def send_file(self):
        # Odeslání souboru na server
        with open(self.file_path, 'rb') as file:
            file_data = file.read()
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            body = (
                '--' + boundary + '\r\n'
                'Content-Disposition: form-data; name="file"; filename="record.wav"\r\n'
                'Content-Type: audio/wav\r\n\r\n' +
                file_data + '\r\n'
                '--' + boundary + '--\r\n'
            )

            headers = {
                'Content-Type': 'multipart/form-data; boundary=' + boundary,
                'Content-Length': str(len(body))
            }

            request = urllib2.Request(self.api_url, body, headers)

            try:
                response = urllib2.urlopen(request)
                response_data = json.loads(response.read())
                ai_completion = response_data['response']
                ai_completion = ai_completion.encode('utf-8')  # Encode to UTF-8 for printing
                self.tts.say(ai_completion)
                self.logger.fatal(response.read())

            except urllib2.HTTPError as e:
                self.logger.fatal(e.reason)
                print('HTTP Error:', e.code, e.reason)
            except urllib2.URLError as e:
                self.logger.fatal(e.reason)
                print('URL Error:', e.reason)
