import os
from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

# 입력 이미지 경로
input_image_path = './VisionStudy/projectData/normal/26309_000_OK.jpeg'

# 모델 로드
model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)

# CPU 사용 설정
device = 'cpu'
model.to(device)
model.eval()

# 데이터 변환 설정
image_size = (1024, 1024)
transform_image = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 이미지 로드 및 변환
image = Image.open(input_image_path).convert("RGB")
input_images = transform_image(image).unsqueeze(0).to(device)

# 예측 수행
with torch.no_grad():
    preds = model(input_images)[-1].sigmoid().cpu()
pred = preds[0].squeeze()

# 마스크 생성
pred_pil = transforms.ToPILImage()(pred)
mask = pred_pil.resize(image.size)
image.putalpha(mask)

# 출력 폴더 확인 및 저장
output_dir = "./rmbg_result"
os.makedirs(output_dir, exist_ok=True)
image.save(os.path.join(output_dir, "no_bg_image.png"))

print("배경 제거된 이미지가 저장되었습니다.")
