from ultralytics import YOLO

model = YOLO("yolov8m.pt")

model.train(
    data="dataset/data.yaml",   # ← 같은 디렉토리 기준이므로 이걸로 OK
    epochs=30,
    imgsz=640
)
