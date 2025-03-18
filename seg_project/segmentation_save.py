import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

# 입력 및 출력 디렉토리 설정
input_dir = "./projectData/normal/"
output_dir = "./projectData/segmentation_results/"

os.makedirs(output_dir, exist_ok=True)  # 출력 폴더 생성

# 이미지 파일 목록 가져오기
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# 모든 이미지 처리
for image_file in image_files:
    image_path = os.path.join(input_dir, image_file)
    save_path = os.path.join(output_dir, os.path.splitext(image_file)[0] + "_otsu.png")

    print(f"Processing: {image_path} → {save_path}")

    # 이미지 불러오기 (Grayscale)
    img = cv2.imread(image_path, 0)

    # 가우시안 블러 적용
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    # Otsu 이진화 적용
    _, th1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 처리된 이미지 저장
    Image.fromarray(th1).save(save_path)


print("✅ 모든 이미지 Otsu 이진화 완료! 결과는 segmentation_results 폴더에 저장되었습니다.")
