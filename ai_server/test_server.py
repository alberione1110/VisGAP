# ai_server/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
import numpy as np
import cv2
import io

app = FastAPI()

@app.post("/process-images")
async def process_images(files: List[UploadFile] = File(...)):
    file = files[0]  # 여러 파일 중 첫 번째 파일만 처리
    contents = await file.read()

    # [✅] 메모리 버퍼를 이미지로 변환
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # [✅] 이진화 처리
    ret1, th1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # [✅] 메모리 버퍼에 JPEG로 인코딩
    _, encoded_img = cv2.imencode('.jpg', th1)

    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
