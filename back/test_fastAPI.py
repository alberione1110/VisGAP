# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import List

app = FastAPI()

# [✅] CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프론트 주소만 제한할 수도 있지만, 개발 단계에선 * (모두 허용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI 서버 주소
AI_SERVER_URL = "http://localhost:8001/process-images"

# 파일 업로드 엔드포인트
@app.post("/upload")
async def upload_images(files: List[UploadFile] = File(...)):
    ai_files = []
    for file in files:
        content = await file.read()
        ai_files.append(('files', (file.filename, content, file.content_type)))

    response = requests.post(AI_SERVER_URL, files=ai_files)
    return response.json()
