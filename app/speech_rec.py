import time
import speech_recognition as sr
from openai_client import log_time



def speech_to_text(file_path: str) -> str:
    recognizer = sr.Recognizer()
    
    log_time("Starting speech recognition.")
    start_time = time.perf_counter()
    
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='cs-CZ')
    
    transcription_time = time.perf_counter() - start_time
    log_time(f"Speech recognition completed. Time taken: {transcription_time:.2f} seconds")
    
    return text