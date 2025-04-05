from PIL import Image
import torch
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import os

# ✅ 이미지 경로 설정
input_image_path = "./projectData/normal/26309_000_OK.jpeg"
if not os.path.exists(input_image_path):
    raise FileNotFoundError(f"이미지 경로가 존재하지 않습니다: {input_image_path}")

# ✅ 장치 설정
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
original_image = Image.open(input_image_path).convert("RGB")
input_tensor = transform_image(original_image).unsqueeze(0).to(device)

# ✅ 배경 제거 예측
with torch.no_grad():
    preds = model(input_tensor)[-1].sigmoid().cpu()

# ✅ 마스크 처리
pred = preds[0].squeeze()
pred_pil = transforms.ToPILImage()(pred)
mask = pred_pil.resize(original_image.size).convert("L")  # 그레이스케일 마스크

# ✅ 흰색 배경 이미지 생성
white_bg = Image.new("RGB", original_image.size, (255, 255, 255))

# ✅ 원본 이미지와 마스크를 이용해 흰색 배경 합성
composite = Image.composite(original_image, white_bg, mask)

# ✅ 결과 보여주기
composite.show()
