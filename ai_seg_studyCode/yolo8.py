import cv2
from ultralytics import YOLO
import numpy as np

# 모델 로드
model = YOLO("runs/detect/train63/weights/best.pt")

# 클래스 이름 리스트 가져오기
class_names = model.names  # 예: {0: 'gap', 1: 'frame', 2: 'magnetic'}

# 추론
results = model.predict(source="./projectData/normal/26309_000_OK.jpeg", save=False, conf=0.1, iou=0.3)

# 결과 처리
for result in results:
    img = result.orig_img.copy()
    boxes = result.boxes
    for box in boxes:
        cls_id = int(box.cls[0].item())
        cls_name = class_names[cls_id]

        if cls_name != "gap":
            continue  # gap이 아니면 스킵

        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        x1, y1, x2, y2 = xyxy
        height = y2 - y1  # GAP의 높이 (세로 픽셀 길이)

        # 바운딩 박스 및 GAP 높이 출력
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f"{height}px", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 결과 띄우기
    cv2.imshow("GAP Height in Pixels", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
