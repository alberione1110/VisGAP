import cv2
import numpy as np

# 이미지 로드
img = cv2.imread('./projectData/normal/26939_000_OK.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 이진화
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# 컨투어 검출
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 가장 큰 사각형 찾기 (y<500 제한 포함)
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
    cv2.rectangle(color_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # 중심 좌표
    center_x = x + w // 2
    center_y = y + h // 2

    # 새로 만들 crop 영역 (2:1 비율)
    new_w = w
    new_h = w // 3.5

    # crop 좌표 계산
    new_x = max(center_x - new_w // 2, 0)
    new_y = max(center_y - new_h // 2, 0)

    # crop 영역이 이미지 넘어가지 않게 조정
    new_x = min(new_x, img.shape[1] - new_w)
    new_y = min(new_y, img.shape[0] - new_h)

    # 최종 crop
    cropped = img[int(new_y):int(new_y+new_h), int(new_x):int(new_x+new_w)]

    # 결과 출력
    cv2.imshow('Biggest Rectangle (full image)', color_img)
    cv2.imshow('Cropped 2:1 Rectangle', cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("검출된 사각형이 없습니다.")
