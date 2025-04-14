import cv2
import numpy as np

# 이미지 로드
img = cv2.imread('./projectData/normal/26939_000_OK.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 관심영역 Crop
crop_x, crop_y, crop_w, crop_h = 300, 300, 600, 180
roi = gray[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]

# 밝은 영역 제거 (Threshold)
_, roi_thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY_INV)  
# 밝은 부분(>200)은 0, 나머지는 255로 반전 → 검은 영역만 강조

# 어두운 부분만 남은 상태에서 Canny Edge
edges = cv2.Canny(roi_thresh, 50, 150)

# Morphology Close로 끊긴 부분 이어주기
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 1))
edges_closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# 컨투어 검출
contours, _ = cv2.findContours(edges_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

roi_color = cv2.cvtColor(roi, cv2.COLOR_GRAY2BGR)
color_img = img.copy()

pixel_to_cm = 0.1

# 검출 결과 표시
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    if w > 30 and w/h > 2 and h > 5:
        cv2.rectangle(roi_color, (x, y), (x+w, y+h), (0,255,0), 2)

        x_global = x + crop_x
        y_global = y + crop_y

        cv2.rectangle(color_img, (x_global, y_global), (x_global+w, y_global+h), (0,255,0), 2)
        gap_cm = h * pixel_to_cm
        cv2.putText(color_img, f"{gap_cm:.2f} cm", (x_global, y_global-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# 결과 출력
cv2.imshow('Cropped ROI Detection (Masked)', roi_color)
#cv2.imshow('Final Result', color_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
