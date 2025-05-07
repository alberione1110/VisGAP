import sys
import os
import zipfile
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout
from ultralytics import YOLO

model = YOLO("runs/detect/train63/weights/best.pt")
class_names = model.names
TARGET_CLASSES = ['frame', 'magnetic']

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VisGAP 이미지 처리기')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()
        self.label = QLabel('이미지를 선택하세요.')
        layout.addWidget(self.label)

        self.button = QPushButton('이미지 선택 및 처리')
        self.button.clicked.connect(self.process_images)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def process_images(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg)")
        if not paths:
            return

        result_dir = "processed_results"
        gap_dir = os.path.join(result_dir, "gap_img")
        seg_dir = os.path.join(result_dir, "seg_img")
        os.makedirs(gap_dir, exist_ok=True)
        os.makedirs(seg_dir, exist_ok=True)

        gap_log = ""

        for idx, path in enumerate(paths):
            img = cv2.imread(path)
            if img is None:
                continue

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
                    elif cls_name in TARGET_CLASSES:
                        color = (0, 255, 0) if cls_name == "frame" else (255, 0, 0)
                        overlay[y1:y2, x1:x2] = cv2.addWeighted(
                            seg_view[y1:y2, x1:x2], 0.5,
                            np.full_like(seg_view[y1:y2, x1:x2], color, dtype=np.uint8), 0.5, 0
                        )
                        cv2.putText(overlay, cls_name, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            base = os.path.splitext(os.path.basename(path))[0]
            gap_path = os.path.join(gap_dir, f"{base}_gap.jpg")
            seg_path = os.path.join(seg_dir, f"{base}_seg.jpg")
            cv2.imwrite(gap_path, gap_view)
            cv2.imwrite(seg_path, overlay)
            gap_log += f"{base} gap = {gap_heights}\n"

        if len(paths) == 1:
            cv2.imshow("GAP View", cv2.imread(gap_path))
            cv2.imshow("Segmentation View", cv2.imread(seg_path))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.label.setText("한 장 처리 완료!")
        else:
            log_path = os.path.join(result_dir, "gaps.txt")
            with open(log_path, 'w') as f:
                f.write(gap_log)

            zip_path = os.path.join(result_dir, "results.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for folder, name in [(gap_dir, "gap_img"), (seg_dir, "seg_img")]:
                    for f in os.listdir(folder):
                        file_path = os.path.join(folder, f)
                        arc_name = os.path.join(name, f)
                        zipf.write(file_path, arcname=arc_name)
                zipf.write(log_path, arcname="gaps.txt")

            self.label.setText(f"여러 장 처리 완료! ZIP 저장: {zip_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    processor = ImageProcessor()
    processor.show()
    sys.exit(app.exec_())
