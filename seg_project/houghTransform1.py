import numpy as np
import cv2

image = cv2.imread("./projectData/segmentation_results/26309_000_OK_otsu.png")
# 원본 영상을 복사
image2 = image.copy()

# 흑백 영상으로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# canny edge detection을 이용해 edge 검출
edges = cv2.Canny(gray, 100, 200)

# HoughLines 함수를 이용해 직선 정보를 저장 
lines = cv2.HoughLines(edges, 1, np.pi/180, 80)

# 출력된 직선 정보를 이용해 원본 사진에 표현 
for line in lines:
    rho, theta = line[0]
    cos, sin = np.cos(theta), np.sin(theta)
    cx, cy = rho * cos, rho * sin
    x1, y1 = int(cx + 1000 * (-sin)), int(cy + 1000 * cos)
    x2, y2 = int(cx + 1000 * sin), int(cy + 1000 * (-cos))
    # 원본 사진에 초록색 선으로 표시
    cv2.line(image2, (x1, y1), (x2, y2), (0,255,0), 1)

# 에지 검출 영상 출력
cv2.imshow("image", image2)
# 직선 검출 영상 출력
cv2.imshow("edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows() # 모든 창 닫기
cv2.waitKey(1)
print(1)