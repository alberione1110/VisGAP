import cv2
import numpy as np

# 이미지 로드
img = cv2.imread('./projectData/normal/26939_000_OK.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 이진화
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# 컨투어 검출
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 가장 큰 사각형 찾기 (y < 500 제한)
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
    # 초록 네모 (마그네틱)
    x, y, w, h = best_rect

    # 빨간 네모 (확장된 3.5:1 사각형)
    center_x = x + w // 2
    center_y = y + h // 2
    red_w = w
    red_h = int(w / 3.5)
    red_x = int(center_x - red_w // 2)
    red_y = int(center_y - red_h // 2)

    red_x = max(0, min(red_x, img.shape[1] - red_w))
    red_y = max(0, min(red_y, img.shape[0] - red_h))

    # 파란 네모 1 (위쪽 GAP)
    top1 = min(y, red_y)
    bottom1 = max(y, red_y)
    cv2.rectangle(color_img, (red_x, top1), (red_x + red_w, bottom1), (255, 0, 0), 2)
    gap1_px = bottom1 - top1

    # 파란 네모 2 (아래쪽 GAP)
    green_bottom = y + h
    red_bottom = red_y + red_h
    top2 = min(green_bottom, red_bottom)
    bottom2 = max(green_bottom, red_bottom)
    cv2.rectangle(color_img, (red_x, top2), (red_x + red_w, bottom2), (255, 0, 0), 2)
    gap2_px = bottom2 - top2

    # 텍스트 출력 (픽셀 단위)
    cv2.putText(color_img, f"{gap1_px} px", (red_x + 5, top1 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(color_img, f"{gap2_px} px", (red_x + 5, top2 + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # 결과 출력
    cv2.imshow('GAP Measurement (Pixel)', color_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("검출된 사각형이 없습니다.")
