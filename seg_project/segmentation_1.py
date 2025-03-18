import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# ✅ 1. 이미지 로드 및 Grayscale 변환
def preprocess_image(image_path):
    image = cv2.imread(image_path)  # BGR 형식으로 로드
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Grayscale 변환
    return image, gray

# ✅ 2. 대비 조절 + Gaussian Blur (빛 번짐 완화)
def enhance_contrast(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)  # 노이즈 제거
    equalized = cv2.equalizeHist(blurred)  # 히스토그램 평활화 (대비 증가)
    return equalized

# ✅ 3. Adaptive Thresholding (더 정확한 배경 제거)
def apply_threshold(image):
    # 적응형 Thresholding (지역 대비를 고려하여 배경과 금속 분리)
    binary_mask = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # 어두운 배경과 금속 부분을 분리하는 추가 Thresholding
    _, dark_mask = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)

    # 중간 밝기 부분(반사 영역) → 배경과 금속 사이 영역
    middle_mask = cv2.bitwise_and(~binary_mask, ~dark_mask)

    return binary_mask, dark_mask, middle_mask

# ✅ 4. Canny Edge Detection (경계 강화)
def apply_edge_detection(image):
    edges = cv2.Canny(image, 50, 150)  # Canny Edge 적용
    return edges

# ✅ 5. 컬러 마스크 적용 (배경 → 빨간색, 금속 → 흰색, 중간 → 파란색)
def apply_color_mask(image, bright_mask, dark_mask, middle_mask):
    # 컬러 마스크 초기화
    color_mask = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    # 배경 (검은 부분 → 빨간색으로 변경)
    color_mask[dark_mask == 255] = [255, 0, 0]  # Red

    # 금속 부분 (밝은 부분 → 흰색 유지)
    color_mask[bright_mask == 255] = [255, 255, 255]  # White

    # 중간 영역 (회색 영역 → 파란색)
    color_mask[middle_mask == 255] = [0, 0, 255]  # Blue

    return color_mask

# ✅ 6. 원본 이미지에 마스크 Overlay
def overlay_mask_on_image(image, color_mask, alpha=0.5):
    overlay = cv2.addWeighted(image, 1 - alpha, color_mask, alpha, 0)
    return overlay

# ✅ 7. 최종 세그멘테이션 수행 및 시각화
def segment_and_visualize(image_path):
    image, gray_image = preprocess_image(image_path)  # Grayscale 변환
    enhanced_image = enhance_contrast(gray_image)  # 대비 증가
    bright_mask, dark_mask, middle_mask = apply_threshold(enhanced_image)  # Thresholding
    edges = apply_edge_detection(enhanced_image)  # 경계 검출
    color_mask = apply_color_mask(image, bright_mask, dark_mask, middle_mask)  # 컬러 마스크 적용
    overlayed_image = overlay_mask_on_image(image, color_mask)  # 마스크 Overlay

    # 원본 이미지 로드 (RGB 변환)
    original_image = Image.open(image_path).convert("RGB")

    # 결과 시각화
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 4, 1)
    plt.imshow(original_image)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 4, 2)
    plt.imshow(color_mask)
    plt.title("Segmentation Mask (Colored)")
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.imshow(edges, cmap="gray")
    plt.title("Edge Detection")
    plt.axis("off")

    plt.subplot(1, 4, 4)
    plt.imshow(overlayed_image)
    plt.title("Overlayed on Original")
    plt.axis("off")

    plt.show()

# ✅ 테스트 실행
test_image_path = "./projectData/segmentation_results/26309_000_OK_otsu.png"  # 원하는 이미지 경로 입력
segment_and_visualize(test_image_path)

test_image_path = "./projectData/normal/26309_000_OK.jpeg"  # 원하는 이미지 경로 입력
segment_and_visualize(test_image_path)