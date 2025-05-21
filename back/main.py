# main.py (backend/main.py)

import os
import io
import zipfile
import time
from typing import List

from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from ai_utils import process_image_bytes

app = FastAPI()

# CORS 설정 (개발환경: 모든 오리진 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['X-Processing-Time'],
)

# 결과 이미지 제공을 위한 static 폴더 마운트
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.post('/api/upload')
async def upload_single(
    request: Request,
    file: UploadFile = File(...)
):
    """
    단일 이미지 업로드 처리
    - PNG 바이트로 인코딩된 segmentation, gap 이미지를 disk에 저장
    - 모든 gap 높이 리스트를 JSON 으로 반환
    """
    # 1) 파일 형식 체크
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, '이미지 파일만 업로드 가능합니다.')

    # 2) 바이트 읽기 & 처리 시간 측정
    data = await file.read()
    start_time = time.time()

    # 3) AI 처리
    seg_bytes, gap_bytes, gap_values = process_image_bytes(data)
    elapsed = round(time.time() - start_time, 3)

    # 4) 파일명 준비
    name, _ = os.path.splitext(file.filename)

    # 5) 저장 폴더 생성
    seg_dir = os.path.join('static', 'segmentation')
    gap_dir = os.path.join('static', 'gap')
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(gap_dir, exist_ok=True)

    # 6) 디스크에 쓰기
    with open(os.path.join(seg_dir, f'{name}.png'), 'wb') as f:
        f.write(seg_bytes)
    with open(os.path.join(gap_dir, f'{name}.png'), 'wb') as f:
        f.write(gap_bytes)

    # 7) full URL 조합
    base = str(request.base_url).rstrip('/')
    segmentation_url = f'{base}/static/segmentation/{name}.png'
    gap_url          = f'{base}/static/gap/{name}.png'

    # 8) JSON 응답
    return JSONResponse({
        'type': 'single',
        'segmentationUrl': segmentation_url,
        'gapUrl':          gap_url,
        'gapValue':        gap_values,   # 리스트 형태로 전달
        'time':             elapsed
    })


@app.post('/api/upload-multiple')
async def upload_multiple(
    files: List[UploadFile] = File(...)
):
    """
    다중 이미지 업로드 처리
    - 각 이미지에 대해 segmentation, gap PNG를 ZIP으로 압축하여 스트리밍 응답
    """
    # 1) 파일 유효성 체크
    if any(not f.content_type.startswith('image/') for f in files):
        raise HTTPException(400, '이미지 파일만 업로드 가능합니다.')

    # 2) ZIP 생성 & 처리 시간 측정
    start_time = time.time()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        for f in files:
            data = await f.read()
            seg_b, gap_b, _ = process_image_bytes(data)
            base, _ = os.path.splitext(f.filename)
            zf.writestr(f'{base}_seg.png', seg_b)
            zf.writestr(f'{base}_gap.png', gap_b)
    elapsed = round(time.time() - start_time, 3)
    buf.seek(0)

    # 3) ZIP 스트리밍 응답
    return StreamingResponse(
        buf,
        media_type='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename="results.zip"',
            'X-Processing-Time': str(elapsed)
        }
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
