import cv2
import numpy as np

# ✅ 선 길이 필터링
def filter_lines_by_length(lines, min_length=70):
    filtered = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = np.hypot(x2 - x1, y2 - y1)
        if length >= min_length:
            filtered.append(line)
    return filtered

# ✅ 수평선 필터링 (기울기 필터링)
def filter_lines_by_angle(lines, min_angle=0, max_angle=10):
    filtered = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        angle = abs(angle)
        if (min_angle <= angle <= max_angle) or (170 <= angle <= 180):
            filtered.append(line)
    return filtered

# ✅ y좌표 범위 필터링
def filter_lines_by_y_range(lines, min_y=100, max_y=500):
    filtered = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cy = (y1 + y2) // 2
        if min_y <= cy <= max_y:
            filtered.append(line)
    return filtered

# ✅ 가까운 선끼리 비교해서 긴 선만 남기는 필터
def filter_lines_by_proximity_and_length_y_only(lines, merge_threshold=5, length_ratio_threshold=0.7):
    lines = sorted(lines, key=lambda line: (line[0][1] + line[0][3]) // 2)  # y중심 정렬
    result = []
    used = [False] * len(lines)

    for i in range(len(lines)):
        if used[i]:
            continue
        x1a, y1a, x2a, y2a = lines[i][0]
        cy1 = (y1a + y2a) // 2
        len1 = np.hypot(x2a - x1a, y2a - y1a)

        for j in range(i+1, len(lines)):
            if used[j]:
                continue
            x1b, y1b, x2b, y2b = lines[j][0]
            cy2 = (y1b + y2b) // 2
            len2 = np.hypot(x2b - x1b, y2b - y1b)

            # ✅ y중심 거리만 비교
            if abs(cy1 - cy2) <= merge_threshold:
                # ✅ 길이 차이 비율 확인
                if len1 >= len2:
                    if len2 / len1 < length_ratio_threshold:
                        used[j] = True
                else:
                    if len1 / len2 < length_ratio_threshold:
                        used[i] = True
                        break

        if not used[i]:
            result.append(lines[i])

    return result


# ✅ 1. 이미지 로드 및 이진화
img = cv2.imread('./projectData/normal/26939_000_OK.jpeg', 0)
blur = cv2.GaussianBlur(img, (5, 5), 0)
_, th2 = cv2.threshold(blur, 130, 255, cv2.THRESH_BINARY)

# ✅ 2. 엣지 검출
edges = cv2.Canny(th2, 50, 150)

# ✅ 3. 허프라인 검출
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=30, maxLineGap=10)

# ✅ 4. 선 필터링
if lines is not None:
    lines = filter_lines_by_length(lines, min_length=70)
    lines = filter_lines_by_angle(lines, min_angle=0, max_angle=10)
    lines = filter_lines_by_y_range(lines, min_y=300, max_y=470)

    # ✅ 5. 가까운 선 중 긴 선만 남기기
    lines = filter_lines_by_proximity_and_length_y_only(lines, merge_threshold=5, length_ratio_threshold=0.7)

    # ✅ 6. 초록색 선 먼저 그리기 + 중심점 리스트 생성
    color_img = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)
    centers = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(color_img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 초록색 선
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        centers.append((cx, cy))

    # ✅ 7. 모든 쌍 거리 계산
    distances = []
    for i in range(len(centers)):
        for j in range(i+1, len(centers)):
            cx1, cy1 = centers[i]
            cx2, cy2 = centers[j]

            y_distance = abs(cy1 - cy2)
            distances.append((y_distance, (cx1, cy1, cx2, cy2)))

    # ✅ 8. 거리 짧은 순 정렬 후 Top-6 선택
    distances = sorted(distances, key=lambda x: x[0])

    pixel_to_cm = 0.1  # 변환 비율: 10픽셀 = 1cm

    for idx, (dist, (x1, y1, x2, y2)) in enumerate(distances[:6]):
        x_mid = (x1 + x2) // 2

        pt1 = (x_mid, y1)
        pt2 = (x_mid, y2)

        real_distance = dist * pixel_to_cm
        mid_point = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)

        # ✅ 거리 연결 및 표시 (빨간색)
        cv2.line(color_img, pt1, pt2, (0, 0, 255), 2)
        cv2.putText(color_img, f"{real_distance:.2f} cm", mid_point,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# ✅ 9. 결과 출력
cv2.imshow("Filtered by Length Priority", color_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
