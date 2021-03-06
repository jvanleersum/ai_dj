from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from ai_dj import params
from google.cloud import storage
import io
import os
from ai_dj.trainer import get_mix

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index(filename):
    #?filename=1019315 Guido Sava - Fever (Original Mix).wav
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    blob = bucket.blob(f'data/audio_wav/1019315 Guido Sava - Fever (Original Mix).wav')
    bts = blob.download_as_bytes()
    stream = io.BytesIO(bts)

    return StreamingResponse(stream, media_type="audio/wav")


@app.get('/get-youtube')
def get_youtube(url):
    bucket_location = get_mix(url)
    bucket_folder, bucket_file = os.path.split(bucket_location)

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_folder)
    blob = bucket.blob(bucket_file)
    bts = blob.download_as_bytes()
    stream = io.BytesIO(bts)

    return StreamingResponse(stream, media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

