from ultralytics import YOLO

def main():
    model = YOLO("yolov8m.pt")  # 모델 불러오기
    model.train(
        data="dataset/data.yaml",
        epochs=30,
        imgsz=1024,
        device="cuda",
        name="train6"
    )

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()  # Windows multiprocessing 문제 해결용
    main()
