import cv2
import numpy as np
import os
from glob import glob

# 입력 및 출력 경로
input_dir = './projectData/normal'
output_dir = './projectData/result'
os.makedirs(output_dir, exist_ok=True)

# 이미지 파일 리스트 불러오기
image_files = glob(os.path.join(input_dir, '*.jpeg'))

for image_path in image_files:
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    best_rect = None
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if y < 500 and area > max_area:
            max_area = area
            best_rect = (x, y, w, h)

    color_img = img.copy()
    if best_rect:
        x, y, w, h = best_rect

        center_x = x + w // 2
        center_y = y + h // 2
        red_w = w
        red_h = int(w / 3.5)
        red_x = int(center_x - red_w // 2)
        red_y = int(center_y - red_h // 2)
        red_x = max(0, min(red_x, img.shape[1] - red_w))
        red_y = max(0, min(red_y, img.shape[0] - red_h))

        top1 = min(y, red_y)
        bottom1 = max(y, red_y)
        cv2.rectangle(color_img, (red_x, top1), (red_x + red_w, bottom1), (255, 0, 0), 2)
        gap1_px = bottom1 - top1

        green_bottom = y + h
        red_bottom = red_y + red_h
        top2 = min(green_bottom, red_bottom)
        bottom2 = max(green_bottom, red_bottom)
        cv2.rectangle(color_img, (red_x, top2), (red_x + red_w, bottom2), (255, 0, 0), 2)
        gap2_px = bottom2 - top2

        cv2.putText(color_img, f"{gap1_px} px", (red_x + 5, top1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(color_img, f"{gap2_px} px", (red_x + 5, top2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 결과 이미지 저장
    filename = os.path.basename(image_path)
    save_path = os.path.join(output_dir, f"result_{filename}")
    cv2.imwrite(save_path, color_img)

print("모든 이미지 처리 및 저장 완료.")
