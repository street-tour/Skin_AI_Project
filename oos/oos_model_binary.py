import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import numpy as np

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.skip_connection = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.skip_connection = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        identity = self.skip_connection(x)
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += identity
        return F.relu(out)

class SkinNet(nn.Module):
    def __init__(self):
        super(SkinNet, self).__init__()

        self.initial_conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        self.res_block1 = ResidualBlock(64, 128, stride=2)
        self.res_block2 = ResidualBlock(128, 256, stride=2)
        self.res_block3 = ResidualBlock(256, 512, stride=2)

        self.depthwise_conv = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding=1, groups=512),
            nn.Conv2d(512, 1024, kernel_size=1),
            nn.BatchNorm2d(1024),
            nn.ReLU()
        )

        self.gap = nn.AdaptiveAvgPool2d(1)
        self.dropout = nn.Dropout(0.4)
        self.bn_fc = nn.BatchNorm1d(1024)
        self.fc = nn.Linear(1024, 1)  # 출력 노드를 1로 변경
        self.sigmoid = nn.Sigmoid()  # 시그모이드 활성화 함수 추가

    def forward(self, x):
        x = self.initial_conv(x)
        x = self.res_block1(x)
        x = self.res_block2(x)
        x = self.res_block3(x)
        x = self.depthwise_conv(x)
        x = self.gap(x)
        x = torch.flatten(x, 1)
        x = self.bn_fc(x)
        x = self.dropout(x)
        x = self.fc(x)
        x = self.sigmoid(x)  # Sigmoid 활성화 적용
        return x






# 전처리 함수
def preprocess_input(image):
    """
    Args:
        image (PIL.Image 또는 numpy.ndarray): 입력 이미지
    Returns:
        torch.Tensor: 전처리된 이미지 텐서
    """
    # numpy.ndarray일 경우
    if isinstance(image, np.ndarray):
        # 데이터 타입 변환 (float64 → uint8)
        if image.dtype != np.uint8:
            image = (image * 255).astype(np.uint8)  # 0~1 범위라면 0~255로 스케일링
        
        # 배열의 크기 확인
        if len(image.shape) == 3 and image.shape[0] == 1:  # (1, H, W, C) 형상일 경우
            image = np.squeeze(image, axis=0)  # 첫 번째 차원 제거

        # PIL.Image로 변환
        image = Image.fromarray(image)

    # 전처리 순서: Resize → ToTensor
    transform = transforms.Compose([
        transforms.Resize((128, 128)),  # 크기 조정
        transforms.ToTensor()          # 텐서로 변환
    ])

    # 전처리 적용
    processed_image = transform(image)

    # 배치 차원 추가
    processed_image = processed_image.unsqueeze(0)  # shape: (1, C, H, W)

    return processed_image





def predict(image, model, device='cpu'):
    
    """
    Args:
        image (PIL.Image 또는 numpy.ndarray): 입력 이미지
        model (torch.nn.Module): 학습된 모델
        device (str): 'cpu' 또는 'cuda'
    Returns:
        tuple: (결과 클래스 (0 또는 1), 신뢰도 (확률 값))
    """
    # 모델을 평가 모드로 전환
    model = model
    model.eval()
    model.to(device)

    # 입력 이미지를 전처리
    processed_image = preprocess_input(image)
    processed_image = processed_image.to(device)

    # 모델에 입력하여 예측
    with torch.no_grad():
        output = model(processed_image)

    # 결과 값과 신뢰도 추출
    
    confidence = output.item()  # Sigmoid 값
    confidence_percentage = max(confidence, 1 - confidence) * 100  # 신뢰도 계산
    predicted_class = 1 if confidence >= 0.5 else 0  # 0.5 기준으로 클래스 분류

    return predicted_class, confidence_percentage

