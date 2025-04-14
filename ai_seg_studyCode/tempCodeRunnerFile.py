import cv2
import numpy as np

# ✅ 1. 이미지 로드
img = cv2.imread('./projectData/normal/26939_000_OK.jpeg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ✅ 2. 블러 처리 + 약한 이진화 (어두운 부분 강조)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
_, binary = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)

# ✅ 3. 컨투어 검출
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# ✅ 4. 박스 그리고 + GAP(cm) 표시
color_img = img.copy()
pixel_to_cm = 0.1  # 변환 비율

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # 박스 그리기
    cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # GAP 계산
    gap_pixel = h
    gap_cm = gap_pixel * pixel_to_cm

    # GAP 값 표시
    cv2.putText(color_img, f"{gap_cm:.2f} cm", (x, y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# ✅ 5. 결과 출력
cv2.imshow("Contours with GAP (No Filtering)", color_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
