import tensorflow as tf
import torch
import os
from PIL import Image
import numpy as np

# 모델을 저장할 캐시
model_cache = {}

def load_model(model_name):
    if model_name not in model_cache:
        model_path = get_model_path(model_name)
        if model_path.endswith('.h5'):  # TensorFlow 모델
            model = tf.keras.models.load_model(model_path)
        elif model_path.endswith('.pth'):  # PyTorch 모델
            model = torch.load(model_path, map_location="cpu")
            model.eval()  # PyTorch 모델의 경우 반드시 eval 모드로 설정
        else:
            raise ValueError("Unsupported model format")
        model_cache[model_name] = model
    return model_cache[model_name]

def get_model_path(model_name):
    model_paths = {
        "이마-주름": "serving_model/model70.h5",
        "이마-색소침착": "serving_model/ForeheadPigmentation_BinaryClassification_Cam_3F_4190.pth",
        "볼": "serving_model/볼모공_분류모델.h5",
        "미간": "serving_model/미간주름_분류모델.h5",
        "턱": "serving_model/턱쳐짐_분류모델.h5",
        "입술": "serving_model/입술건조_분류모델.h5",
        "눈가주름": "serving_model/눈가주름_분류모델.h5",
        "여드름": "serving_model/여드름_분류모델.h5"
    }
    return model_paths.get(model_name, "")
