# ai_server/main.py
from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()

@app.post("/process-images")
async def process_images(files: List[UploadFile] = File(...)):
    filenames = [file.filename for file in files]
    return {"message": "AI 서버 처리 완료", "received_files": filenames}
