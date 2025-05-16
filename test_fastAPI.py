# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests
import io
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AI_SERVER_URL = "http://localhost:8001/process-images"

@app.post("/upload")
async def upload_images(files: List[UploadFile] = File(...)):
    ai_files = []
    for file in files:
        content = await file.read()
        ai_files.append(('files', (file.filename, content, file.content_type)))

    response = requests.post(AI_SERVER_URL, files=ai_files)

    # ✨ 받은 이미지를 프론트로 그대로 전달
    return StreamingResponse(io.BytesIO(response.content), media_type="image/jpeg")
