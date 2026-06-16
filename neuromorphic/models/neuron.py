import torch
import torch.nn as nn
import snntorch as snn

class ConvLIF(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride=1, padding=0,
                 beta=0.9, threshold=0.2):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size,
                              stride=stride, padding=padding)
        nn.init.xavier_uniform_(self.conv.weight, gain=7.0)
        nn.init.zeros_(self.conv.bias)
        self.neuron = snn.Leaky(beta=beta, threshold=threshold,
                                learn_beta=True, learn_threshold=True)

    def forward(self, x, mem=None):
        cur = self.conv(x)
        if mem is None:
            mem = torch.zeros_like(cur)
        spk, mem = self.neuron(cur, mem)
        return spk, mem

class LinearLIF(nn.Module):
    def __init__(self, in_features, out_features,
                 beta=0.9, threshold=0.2):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        nn.init.xavier_uniform_(self.linear.weight, gain=4.0)
        nn.init.zeros_(self.linear.bias)
        self.neuron = snn.Leaky(beta=beta, threshold=threshold,
                                learn_beta=False, learn_threshold=False)

    def forward(self, x, mem=None):
        cur = self.linear(x)
        if mem is None:
            mem = torch.zeros_like(cur)
        spk, mem = self.neuron(cur, mem)
        return spk, mem
