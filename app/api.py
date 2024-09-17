# app/api.py
import time
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from services.audio_service import save_audio_file, validate_audio_file
from config import AUDIO_DIR
from speech_rec import speech_to_text
from openai_client import get_response, get_response_stream, get_response_stream_, log_time


# API Router instance
router = APIRouter()

# curl -o /dev/null -s -w "Total time: %{time_total}s\n" http://127.0.0.1:8000/api/v1/
@router.get("/", tags=["default"])
def read_root():
    return JSONResponse(content={"message": "Hello World"})

# curl -o /dev/null -s -w "Total time: %{time_total}s\n" -X POST http://127.0.0.1:8000/api/v1/upload/streamed -F "file=@example.wav"
@router.post("/upload/streamed", tags=["upload/stream"])
async def upload_audio_file_streamed(file: UploadFile = File(...)):

    start_time = time.perf_counter()
    log_time("Starting file upload and processing.")
    validate_audio_file(file)

    await save_audio_file(file, AUDIO_DIR)
    upload_duration = time.perf_counter() - start_time
    log_time(f"File uploaded in {upload_duration:.5f} seconds")

    text = speech_to_text(file_path=AUDIO_DIR + "/" + file.filename)


    log_time("Starting response streaming.")
    return StreamingResponse(get_response_stream(text), media_type="text/plain")

@router.post("/upload/non-streamed", tags=["upload/non-stream"])
async def upload_audio_file_non_streamed(file: UploadFile = File(...)):

    start_time = time.perf_counter()
    log_time("Starting file upload and processing.")
    validate_audio_file(file)

    await save_audio_file(file, AUDIO_DIR)
    upload_duration = time.perf_counter() - start_time
    log_time(f"File uploaded in {upload_duration:.5f} seconds")

    text = speech_to_text(file_path=AUDIO_DIR + "/" + file.filename)

    log_time("Starting non-streamed response.")
    response = get_response(text)

    return JSONResponse(content={"message": "File uploaded successfully", "path": AUDIO_DIR + "/" + file.filename, "transcription": text, "response": response})





# @router.post("/upload/streamed", tags=["upload/stream"])
# async def upload_audio_file(file: UploadFile = File(...)):

#     starttime = time.perf_counter()
#     validate_audio_file(file)

#     await save_audio_file(file, AUDIO_DIR)
#     endTime = time.perf_counter() - starttime
#     # print in miliseconds
#     print(f"File uploaded in: {endTime:.5f} seconds")
    

#     text = speech_to_text(file_path=AUDIO_DIR + "/" + file.filename)

#     return StreamingResponse(get_response_stream(text), media_type="text/plain")



# @router.post("/upload/non-streamed", tags=["upload/non-stream"])
# async def upload_audio_file(file: UploadFile = File(...)):

#     starttime = time.perf_counter()
#     validate_audio_file(file)

#     await save_audio_file(file, AUDIO_DIR)
#     endTime = time.perf_counter() - starttime
#     # print in miliseconds
#     print(f"File uploaded in: {endTime:.5f} seconds")
    

#     text = speech_to_text(file_path=AUDIO_DIR + "/" + file.filename)

#     response = get_response(text)

#     return JSONResponse(content={"message": "File uploaded successfully", "path": AUDIO_DIR + "/" + file.filename, "transcription": text, "response": response})

