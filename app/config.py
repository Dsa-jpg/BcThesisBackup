# Description: Configuration file for the FastAPI application

# Settings for the FastAPI documentation UI
TAGS_METADATA = [
    {
        "name": "upload/non-stream",
        "description": "Operations for uploading audio files without streaming response.",

    },
    {
        "name": "upload/stream",
        "description": "Operations for uploading audio files with streaming response.",

    }
]
CONTACT = {
        "name": "Filip Nachtman",
        "url": "https://github.com/Dsa-jpg",
        "email": "nachtf00@jcu.cz"
        }
APP_TITLE = "Middleware application for Robot NAO"
APP_DESCRIPTION = "This is a simple application to bring the robot NAO to think and speak. "
APP_VERSION = "0.1"
APP_ROOT_PATH = "/api/v1"
SERVERS = [
        {"url": "/api/v1", "description": "Version 1 of the API"},
        {"url": "/api/v2", "description": "Version 2 of the API"}
    ]


# Key for openAI API
OPENAI_API_KEY = "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"

# Path to the directory where the audio files will be stored
AUDIO_DIR = "uploads"


PROMPTMSG = """Jsi robot NAO. Je ti 14 let. A žiješ v Český Budějovicích. 
               Když odpovídáš, formátuj své věty jako lidskou řeč, s přirozenými pauzami po tečkách a čárkách.
               Ujisti se, že tvůj tón je přátelský a konverzační."""


CACHE_EXPIRATION = 60 # seconds

# Redis connection settings
REDIS_HOST = "redis-16198.c328.europe-west3-1.gce.redns.redis-cloud.com"
REDIS_PORT = 16198
REDIS_PASSWORD = "MM4oqGF92U4zZrxTGO5YxWIPlZHNnZWa"
