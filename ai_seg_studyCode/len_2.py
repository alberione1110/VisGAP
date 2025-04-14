import cv2
import numpy as np

image_path = './projectData/normal/26939_000_OK.jpeg'  # 분석할 이미지 경로

# 1. 이미지 로드 및 그레이스케일 이미지 변환
img = cv2.imread(image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 노이즈 제거 (가우시안 블러)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 이진화 (Threshold)
_, binary = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

# 2. 컨투어(윤곽선) 검출
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 3. 후보 영역 필터링
boxes = []
img_area = gray.shape[0] * gray.shape[1]

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    area = w * h

    if area < img_area * 0.1:  # 전체 면적의 10% 이상은 배제
        boxes.append((x, y, w, h))
        
    # 박스 크기 필터링
    if w > 20 and h > 5 and w > h:
        boxes.append((x, y, w, h))

# 박스를 y좌표 기준으로 정렬
boxes = sorted(boxes, key=lambda b: b[1])

# 4. GAP 측정
color_img = img.copy()

for idx, (x, y, w, h) in enumerate(boxes):
    # 박스 그리기
    cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # GAP 계산
    gap_pixel = h

    # GAP 값 텍스트로 표시
    text = f"{gap_pixel:.2f} px"
    text_pos = (x, y - 10)  # 박스 위에 텍스트 표시
    cv2.putText(color_img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# 5. 결과 출력
cv2.imshow('GAP Measurement', color_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# (선택) 결과 저장하기
# cv2.imwrite('./gap_result.png', color_img)
