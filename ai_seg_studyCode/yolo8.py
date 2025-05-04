import cv2
from ultralytics import YOLO
import numpy as np

# 모델 로드
model = YOLO("runs/detect/train11/weights/best.pt")

# 클래스 이름 리스트 가져오기
class_names = model.names  # 예: {0: 'gap', 1: 'frame', 2: 'magnetic'}

# 추론
results = model.predict(source="./projectData/normal/27203_000_OK.jpeg", save=False, conf=0.1, iou=0.3)

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
        conf = box.conf[0].item()

        # 박스 그리기
        cv2.rectangle(img, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
        cv2.putText(img, f"{cls_name} {conf:.2f}", (xyxy[0], xyxy[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 결과 띄우기
    cv2.imshow("Only GAP", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
