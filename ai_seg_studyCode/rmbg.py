from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import os

# ✅ 이미지 경로 설정
input_image_path = "./projectData/normal/26309_000_OK.jpeg"  # 여기에 이미지 파일 경로 입력
if not os.path.exists(input_image_path):
    raise FileNotFoundError(f"이미지 경로가 존재하지 않습니다: {input_image_path}")

# ✅ 장치 설정 (CUDA 사용 가능하면 GPU, 아니면 CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.set_float32_matmul_precision('high')

# ✅ 모델 로딩 및 장치 할당
model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
model.to(device)
model.eval()

# ✅ 이미지 전처리 설정
image_size = (1024, 1024)
transform_image = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# ✅ 이미지 로딩 및 처리
image = Image.open(input_image_path).convert("RGB")
input_tensor = transform_image(image).unsqueeze(0).to(device)

# ✅ 배경 제거 예측
with torch.no_grad():
    preds = model(input_tensor)[-1].sigmoid().cpu()

# ✅ 마스크 처리 및 투명 배경 이미지 생성
pred = preds[0].squeeze()
pred_pil = transforms.ToPILImage()(pred)
mask = pred_pil.resize(image.size)
image.putalpha(mask)

# ✅ 결과 저장
output_path = os.path.splitext(input_image_path)[0] + "_no_bg.png"
image.save(output_path)
print(f"배경 제거된 이미지 저장 완료: {output_path}")