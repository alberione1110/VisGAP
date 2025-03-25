from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import os

# 사용자 이미지 경로 입력
input_image_path = "./projectData/segmentation_results/26309_000_OK_otsu.png"  # 여기에 처리할 이미지 파일명을 입력하세요

# 유효성 검사
if not os.path.exists(input_image_path):
    raise FileNotFoundError(f"입력한 이미지 경로가 존재하지 않습니다: {input_image_path}")

# 모델 불러오기
model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
torch.set_float32_matmul_precision('high')
model.to('cuda')
model.eval()

# 이미지 전처리 정의
image_size = (1024, 1024)
transform_image = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 이미지 불러오기
image = Image.open(input_image_path).convert("RGB")  # RGB로 강제 변환
input_images = transform_image(image).unsqueeze(0).to('cuda')

# 배경 제거 예측
with torch.no_grad():
    preds = model(input_images)[-1].sigmoid().cpu()
pred = preds[0].squeeze()
pred_pil = transforms.ToPILImage()(pred)
mask = pred_pil.resize(image.size)

# 알파 채널에 마스크 적용
image.putalpha(mask)

# 출력 파일명 생성
output_path = os.path.splitext(input_image_path)[0] + "_no_bg.png"
image.save(output_path)
print(f"배경 제거된 이미지가 저장되었습니다: {output_path}")
