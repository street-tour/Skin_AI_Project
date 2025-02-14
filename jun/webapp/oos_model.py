import torch
from PIL import Image
import numpy as np
import warnings
import oos_model_binary as oos

# 경고 무시 (FutureWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)
    # 모델 로드 (구조와 가중치 동시 로드)
    model_path = "/FP_3687(softmax_normalization).pth"
    model = torch.load(model_path, map_location="cpu")
    model.to("cpu")
    model.eval()

# 이미지 경로
path = r"C:\Users\human\Desktop\FP_test.jpg"

# 이미지 로드 및 전처리
image = Image.open(path).convert("RGB")
image_array = np.array(image)
image = image_array / 255  # 0~1로 정규화 (이미지가 numpy 배열인 경우)

# 모델 예측
result, confidence = oos.predict(image=image, model=model)

# 결과 및 신뢰도 출력
if result == 0:
    result_text = "색소침착 없음"
else:
    result_text = "색소침착 심함"

print("=" * 30)
print(f"분석 결과: {result_text}")
print(f"신뢰도: {confidence :.2f}%")
print("=" * 30)
