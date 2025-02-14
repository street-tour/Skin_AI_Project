import torch
import torch.nn as nn
import torch.nn.functional as F

# Model_03
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

# 수정된 SkinNet
class SkinNet(nn.Module):
    def __init__(self):
        super(SkinNet, self).__init__()

        # 초기 Conv 레이어
        self.initial_conv = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )

        # Residual Blocks
        self.res_block1 = ResidualBlock(64, 128, stride=2)
        self.res_block2 = ResidualBlock(128, 256, stride=2)
        self.res_block3 = ResidualBlock(256, 512, stride=2)

        # Depthwise Separable Convolution
        self.depthwise_conv = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, padding=1, groups=512),  # Depthwise
            nn.Conv2d(512, 1024, kernel_size=1),  # Pointwise
            nn.BatchNorm2d(1024),
            nn.ReLU()
        )

        # Global Average Pooling
        self.gap = nn.AdaptiveAvgPool2d(1)

        # Fully Connected Layer with Batch Normalization
        self.dropout = nn.Dropout(0.4)
        self.bn_fc = nn.BatchNorm1d(1024)
        self.fc = nn.Linear(1024, 3)

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

        return x