from ultralytics import YOLO
import cv2
import numpy as np

# detection 모델 로드
model = YOLO("runs/detect/train11/weights/best.pt")

# 예측 수행
results = model.predict(source="./projectData/normal/27203_000_OK.jpeg", conf=0.25, save=False, show=False)

# 클래스 이름과 타겟 클래스 정의
class_names = model.names
target_classes = ['frame', 'magnetic']

# 결과 처리
for r in results:
    img = r.orig_img.copy()
    boxes = r.boxes
    classes = boxes.cls.cpu().numpy()
    xyxy = boxes.xyxy.cpu().numpy()

    overlay = img.copy()

    for i, cls_idx in enumerate(classes):
        cls_name = class_names[int(cls_idx)]
        if cls_name in target_classes:
            x1, y1, x2, y2 = map(int, xyxy[i])
            color = (0, 255, 0) if cls_name == 'frame' else (255, 0, 0)

            # 사각형 영역에 투명한 색상 덧씌우기
            overlay[y1:y2, x1:x2] = cv2.addWeighted(
                img[y1:y2, x1:x2], 0.5,
                np.full_like(img[y1:y2, x1:x2], color, dtype=np.uint8), 0.5, 0
            )

            # 텍스트 넣기
            cv2.putText(overlay, cls_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # 이미지 보기
    cv2.imshow("Transparent Overlay View", overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
