
import os
from fastapi import FastAPI
from config import TAGS_METADATA, CONTACT, APP_TITLE, APP_DESCRIPTION, APP_VERSION, APP_ROOT_PATH, AUDIO_DIR 
from api import router as api_router


os.makedirs(AUDIO_DIR, exist_ok=True)



app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    openapi_tags=TAGS_METADATA,
    contact=CONTACT,
    root_path=APP_ROOT_PATH,
    # servers= None

)


# All routers are included here
app.include_router(api_router)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

