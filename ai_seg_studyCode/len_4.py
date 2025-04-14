import cv2
import numpy as np

# 이미지 로드
img = cv2.imread('./projectData/normal/26939_000_OK.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 이진화 (Threshold)
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# 컨투어 검출
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 가장 큰 사각형 찾기 (y<500 제한 포함)
max_area = 0
best_rect = None

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    area = w * h

    # y가 500 이하인 것만 고려
    if y < 500 and area > max_area:
        max_area = area
        best_rect = (x, y, w, h)

# 원본 이미지에 가장 큰 사각형 그리기
color_img = img.copy()

if best_rect:
    x, y, w, h = best_rect
    cv2.rectangle(color_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

# 결과 출력
cv2.imshow('Biggest Rectangle (y<500)', color_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
