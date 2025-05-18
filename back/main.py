import os, io, zipfile, time
from typing import List
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File

from ai_utils import process_image_bytes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],expose_headers=['X-Processing-Time']
)
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.post('/api/upload')
async def upload_single(request: Request, file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, '이미지 파일만 업로드 가능합니다.')

    data = await file.read()
    start = time.time()
    seg_bytes, gap_bytes, gap_value = process_image_bytes(data)
    elapsed = round(time.time() - start, 3)

    name, _ = os.path.splitext(file.filename)
    seg_dir = os.path.join('static','segmentation')
    gap_dir = os.path.join('static','gap')
    os.makedirs(seg_dir, exist_ok=True)
    os.makedirs(gap_dir, exist_ok=True)

    with open(os.path.join(seg_dir, f'{name}.png'), 'wb') as f:
        f.write(seg_bytes)
    with open(os.path.join(gap_dir, f'{name}.png'), 'wb') as f:
        f.write(gap_bytes)

    base = str(request.base_url).rstrip('/')
    return JSONResponse({
        'type': 'single',
        'segmentationUrl': f'{base}/static/segmentation/{name}.png',
        'gapUrl':          f'{base}/static/gap/{name}.png',
        'gapValue':        int(gap_value) if gap_value is not None else None,
        'time':             elapsed
    })


@app.post('/api/upload-multiple')
async def upload_multiple(files: List[UploadFile] = File(...)):
    # images 키로 오는 경우도 지원
    if not files:
        raise HTTPException(400, '이미지 파일을 업로드 해주세요.')

    start = time.time()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zf:
        for f in files:
            data = await f.read()
            seg_b, gap_b, _ = process_image_bytes(data)
            base, _ = os.path.splitext(f.filename)
            zf.writestr(f'{base}_seg.png', seg_b)
            zf.writestr(f'{base}_gap.png', gap_b)
    elapsed = round(time.time() - start, 3)
    buf.seek(0)

    return StreamingResponse(
        buf,
        media_type='application/zip',
        headers={
            'Content-Disposition': 'attachment; filename="results.zip"',
            'X-Processing-Time': str(elapsed),
        }
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
