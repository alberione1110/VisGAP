# ai_utils.py

import cv2
import numpy as np
from ultralytics import YOLO

# YOLO 모델 로드 (프로젝트 루트 기준 weights 경로로 수정하세요)
model = YOLO("../runs/detect/train63/weights/best.pt")
class_names = model.names
gap_class   = "gap"
seg_classes = ["frame", "magnetic"]

def process_image_bytes(image_bytes: bytes, conf: float = 0.1, iou: float = 0.3):
    """
    이미지 바이트를 받아서
    1) segmentation overlay 이미지 (PNG 바이트)
    2) gap box 그린 이미지 (PNG 바이트)
    3) 모든 gap 높이 리스트 (정수 리스트)
    를 반환합니다.
    """
    # 1) 바이트 → OpenCV BGR 이미지
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    # 2) YOLO 예측
    results = model.predict(source=img, conf=conf, iou=iou, save=False, show=False)

    # 3) 결과용 캔버스 준비
    seg_overlay = img.copy()
    gap_view    = img.copy()
    gap_values  = []  # 모든 gap 높이를 수집할 리스트

    # 4) 예측 박스 순회
    for r in results:
        boxes   = r.boxes
        classes = boxes.cls.cpu().numpy().astype(int)
        coords  = boxes.xyxy.cpu().numpy().astype(int)

        for i, cls_id in enumerate(classes):
            name = class_names[cls_id]
            x1, y1, x2, y2 = coords[i]

            # GAP 클래스인 경우 높이 측정 & 표시
            if name == gap_class:
                height = y2 - y1
                gap_values.append(int(height))
                cv2.rectangle(gap_view, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(
                    gap_view, f"{height}px",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2
                )

            # frame / magnetic 클래스인 경우 세그멘테이션 overlay 처리
            if name in seg_classes:
                color = (0,255,0) if name == "frame" else (255,0,0)
                # 영역 반투명 채우기
                seg_overlay[y1:y2, x1:x2] = cv2.addWeighted(
                    seg_overlay[y1:y2, x1:x2], 0.5,
                    np.full_like(seg_overlay[y1:y2, x1:x2], color, dtype=np.uint8),
                    0.5, 0
                )
                cv2.putText(
                    seg_overlay, name,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
                )

    # 5) PNG 바이트로 인코딩 
    _, seg_buf = cv2.imencode(".png", seg_overlay)
    _, gap_buf = cv2.imencode(".png", gap_view)

    return seg_buf.tobytes(), gap_buf.tobytes(), gap_values
