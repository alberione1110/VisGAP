import cv2
import numpy as np
from ultralytics import YOLO

# 모델 로드
model = YOLO("runs/detect/train63/weights/best.pt")

# 클래스 이름
class_names = model.names
gap_class = 'gap'
seg_classes = ['frame', 'magnetic']

# 이미지 경로
image_path = "./projectData/normal/27203_000_OK.jpeg"

# 모델 예측
results = model.predict(source=image_path, conf=0.1, iou=0.3, save=False, show=False)

for r in results:
    img = r.orig_img.copy()
    gap_view = img.copy()
    seg_view = img.copy()
    boxes = r.boxes
    classes = boxes.cls.cpu().numpy()
    xyxy = boxes.xyxy.cpu().numpy()

    # GAP 바운딩 박스 표시
    for i, cls_idx in enumerate(classes):
        cls_name = class_names[int(cls_idx)]
        if cls_name == gap_class:
            x1, y1, x2, y2 = map(int, xyxy[i])
            height = y2 - y1
            cv2.rectangle(gap_view, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(gap_view, f"{height}px", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 세그멘테이션 대상 오버레이
    overlay = seg_view.copy()
    for i, cls_idx in enumerate(classes):
        cls_name = class_names[int(cls_idx)]
        if cls_name in seg_classes:
            x1, y1, x2, y2 = map(int, xyxy[i])
            color = (0, 255, 0) if cls_name == 'frame' else (255, 0, 0)

            overlay[y1:y2, x1:x2] = cv2.addWeighted(
                seg_view[y1:y2, x1:x2], 0.5,
                np.full_like(seg_view[y1:y2, x1:x2], color, dtype=np.uint8), 0.5, 0
            )
            cv2.putText(overlay, cls_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 이미지 출력
    cv2.imshow("GAP Detection", gap_view)
    cv2.imshow("Segmentation Overlay", overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
