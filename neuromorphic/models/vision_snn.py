import torch
import torch.nn as nn

class VisionSNN(nn.Module):
    def __init__(self, conv_channels=(32, 64, 128), fc_hidden=256, output_dim=6,
                 input_hw=64):
        super().__init__()
        conv_hw = input_hw // 8
        fc_in = conv_channels[-1] * conv_hw * conv_hw
        self.net = nn.Sequential(
            nn.Conv2d(2, conv_channels[0], 5, stride=2, padding=2),
            nn.BatchNorm2d(conv_channels[0]),
            nn.ReLU(),
            nn.Conv2d(conv_channels[0], conv_channels[1], 3, stride=2, padding=1),
            nn.BatchNorm2d(conv_channels[1]),
            nn.ReLU(),
            nn.Conv2d(conv_channels[1], conv_channels[2], 3, stride=2, padding=1),
            nn.BatchNorm2d(conv_channels[2]),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(fc_in, fc_hidden),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(fc_hidden, output_dim),
        )

    def forward(self, x):
        T, B, C, H, W = x.shape
        x = x.mean(dim=0)
        return self.net(x)

    def decode(self, x):
        return x

    def spike_rate(self, x):
        return torch.tensor(0.0)
