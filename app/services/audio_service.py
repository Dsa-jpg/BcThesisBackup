# audio_service.py

import os
from fastapi import HTTPException, UploadFile

async def save_audio_file(file: UploadFile, directory: str) -> str:
    """
    Save the uploaded file to the specified directory
    
    """

    file_path = os.path.join(directory, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return file_path

def validate_audio_file(file: UploadFile) -> None:
    """
    Validate if the file is a valid audio format (.wav or .ogg)
    
    """
    if not (file.filename.endswith('.wav') or file.filename.endswith('.ogg')):
        raise HTTPException(status_code=400, detail="Invalid file type")