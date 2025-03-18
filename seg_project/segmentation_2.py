#기계학습 없이 OpenCV 이미지 전처리 기법 활용
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# ✅ 1. 이미지 로드 및 Grayscale 변환
def preprocess_image(image_path):
    image = cv2.imread(image_path)  # BGR 형식으로 로드
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Grayscale 변환
    return image, gray

# ✅ 2. 대비 조절 (히스토그램 평활화)
def enhance_contrast(image):
    equalized = cv2.equalizeHist(image)  # 히스토그램 평활화
    return equalized

# ✅ 3. Thresholding (이진화) 및 3단계 색상 마스크 생성
def apply_threshold(image, threshold_value=200):
    # 밝은 영역 (금속 부분) → 흰색
    _, bright_mask = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

    # 어두운 영역 (배경 부분) → 검은색
    _, dark_mask = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)

    # 중간 영역 (반사 영역 등) → 회색
    middle_mask = cv2.bitwise_and(~bright_mask, ~dark_mask)

    return bright_mask, dark_mask, middle_mask

# ✅ 4. 컬러 마스크 적용
def apply_color_mask(image, bright_mask, dark_mask, middle_mask):
    # 컬러 마스크 초기화
    color_mask = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    # 배경 (검은 부분 → 빨간색으로 변경)
    color_mask[dark_mask == 255] = [255, 0, 0]  # Red

    # 금속 부분 (밝은 부분 → 흰색 유지)
    color_mask[bright_mask == 255] = [255, 255, 255]  # White

    # 중간 영역 (회색 영역 → 파란색)
    color_mask[middle_mask == 255] = [0, 0, 0]  # Black

    return color_mask

# ✅ 5. 원본 이미지에 마스크 Overlay
def overlay_mask_on_image(image, color_mask, alpha=0.5):
    overlay = cv2.addWeighted(image, 1 - alpha, color_mask, alpha, 0)
    return overlay

# ✅ 6. 최종 세그멘테이션 수행 및 시각화
def segment_and_visualize(image_path):
    image, gray_image = preprocess_image(image_path)  # Grayscale 변환
    enhanced_image = enhance_contrast(gray_image)  # 대비 증가
    bright_mask, dark_mask, middle_mask = apply_threshold(enhanced_image, threshold_value=200)  # 3단계 마스크
    color_mask = apply_color_mask(image, bright_mask, dark_mask, middle_mask)  # 컬러 마스크 적용
    overlayed_image = overlay_mask_on_image(image, color_mask)  # 마스크 Overlay

    # 원본 이미지 로드 (RGB 변환)
    original_image = Image.open(image_path).convert("RGB")

    # 결과 시각화
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.imshow(original_image)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.imshow(color_mask)
    plt.title("Segmentation Mask (Colored)")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.imshow(overlayed_image)
    plt.title("Overlayed on Original")
    plt.axis("off")

    plt.show()

# ✅ 테스트 실행
test_image_path = "./projectData/normal/26939_000_OK.jpeg"  # 원하는 이미지 경로 입력
segment_and_visualize(test_image_path)