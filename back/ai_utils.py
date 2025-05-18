# backend/ai_utils.py
import cv2
import numpy as np
from ultralytics import YOLO

# 모델은 모듈 로드 시 한 번만
model = YOLO("../runs/detect/train63/weights/best.pt")
class_names = model.names
gap_class   = "gap"
seg_classes = ["frame", "magnetic"]

def process_image_bytes(image_bytes: bytes, conf: float = 0.1, iou: float = 0.3):
    # 1) 바이트 → OpenCV 이미지
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    # 2) YOLO 예측 (numpy array 직접 입력 가능)
    results = model.predict(source=img, conf=conf, iou=iou, save=False, show=False)

    # 3) 빈 캔버스 준비
    seg_overlay = img.copy()
    gap_view    = img.copy()
    gap_value   = None

    # 4) 박스 순회하며 세그멘·gap 처리
    for r in results:
        boxes   = r.boxes
        classes = boxes.cls.cpu().numpy().astype(int)
        coords  = boxes.xyxy.cpu().numpy().astype(int)

        for i, cls_id in enumerate(classes):
            x1, y1, x2, y2 = coords[i]
            name = class_names[cls_id]

            # gap 박스 & 높이
            if name == gap_class:
                height = y2 - y1
                gap_value = height
                cv2.rectangle(gap_view, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(gap_view, f"{height}px", (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            # frame/magnetic 세그멘 overlay
            if name in seg_classes:
                color = (0,255,0) if name=="frame" else (255,0,0)
                seg_overlay[y1:y2, x1:x2] = cv2.addWeighted(
                    seg_overlay[y1:y2, x1:x2], 0.5,
                    np.full_like(seg_overlay[y1:y2, x1:x2], color, dtype=np.uint8),
                    0.5, 0)
                cv2.putText(seg_overlay, name, (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 5) 결과 이미지 → PNG 바이트
    _, buf1 = cv2.imencode(".png", seg_overlay)
    _, buf2 = cv2.imencode(".png", gap_view)

    return buf1.tobytes(), buf2.tobytes(), gap_value
