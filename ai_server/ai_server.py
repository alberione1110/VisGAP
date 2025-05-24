from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List
from ultralytics import YOLO
import numpy as np
import cv2
import io
import zipfile
import os

app = FastAPI()
model = YOLO("runs/detect/train63/weights/best.pt")
class_names = model.names

@app.post("/process-smart")
async def process_smart(files: List[UploadFile] = File(...)):
    if len(files) == 1:
        file = files[0]
        content = await file.read()
        npimg = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        results = model.predict(source=img, conf=0.1, iou=0.3, save=False)
        gap_view = img.copy()
        gap_heights = []

        for r in results:
            boxes = r.boxes
            classes = boxes.cls.cpu().numpy()
            xyxy = boxes.xyxy.cpu().numpy()

            for i, cls_id in enumerate(classes):
                cls_name = class_names[int(cls_id)]
                if cls_name != "gap":
                    continue
                x1, y1, x2, y2 = map(int, xyxy[i])
                height = y2 - y1
                gap_heights.append(height)
                cv2.rectangle(gap_view, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(gap_view, f"{height}px", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        _, encoded = cv2.imencode(".jpg", gap_view)
        img_bytes = io.BytesIO(encoded.tobytes())

        return StreamingResponse(
            content=img_bytes,
            media_type="image/jpeg",
            headers={"gap-info": str(gap_heights)}
        )

    else:
        zip_buffer = io.BytesIO()
        gap_log = ""

        with zipfile.ZipFile(zip_buffer, mode="w") as zipf:
            gap_folder = "result/gap_img/"
            seg_folder = "result/seg_img/"
            for folder in [gap_folder, seg_folder]:
                zipf.writestr(folder, "")

            for idx, file in enumerate(files):
                content = await file.read()
                npimg = np.frombuffer(content, np.uint8)
                img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

                results = model.predict(source=img, conf=0.1, iou=0.3, save=False)
                gap_view = img.copy()
                seg_view = img.copy()
                overlay = seg_view.copy()
                gap_heights = []

                for r in results:
                    boxes = r.boxes
                    classes = boxes.cls.cpu().numpy()
                    xyxy = boxes.xyxy.cpu().numpy()

                    for i, cls_id in enumerate(classes):
                        cls_name = class_names[int(cls_id)]
                        x1, y1, x2, y2 = map(int, xyxy[i])
                        if cls_name == "gap":
                            height = y2 - y1
                            gap_heights.append(height)
                            cv2.rectangle(gap_view, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.putText(gap_view, f"{height}px", (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        elif cls_name in ["frame", "magnetic"]:
                            color = (0, 255, 0) if cls_name == "frame" else (255, 0, 0)
                            overlay[y1:y2, x1:x2] = cv2.addWeighted(
                                seg_view[y1:y2, x1:x2], 0.5,
                                np.full_like(seg_view[y1:y2, x1:x2], color, dtype=np.uint8), 0.5, 0
                            )
                            cv2.putText(overlay, cls_name, (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # 이미지 저장
                _, gap_encoded = cv2.imencode(".jpg", gap_view)
                zipf.writestr(f"{gap_folder}{idx}_gap.jpg", gap_encoded.tobytes())

                _, seg_encoded = cv2.imencode(".jpg", overlay)
                zipf.writestr(f"{seg_folder}{idx}_seg.jpg", seg_encoded.tobytes())

                # gap 로그 추가
                gap_log += f"img_{idx} gap = {gap_heights}\n"

            # gap 로그 파일 추가
            zipf.writestr("result/gaps.txt", gap_log)

        zip_buffer.seek(0)
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=results.zip"})