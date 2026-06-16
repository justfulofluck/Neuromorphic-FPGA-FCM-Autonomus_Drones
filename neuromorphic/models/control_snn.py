import torch
import torch.nn as nn
from .neuron import LinearLIF

class ControlSNN(nn.Module):
    def __init__(self, input_dim=6, hidden_dims=(64, 32), output_dim=4,
                 beta=0.95, threshold=0.2, time_steps=20):
        super().__init__()
        self.time_steps = time_steps
        self.fc1 = LinearLIF(input_dim, hidden_dims[0],
                             beta=beta, threshold=threshold)
        self.fc2 = LinearLIF(hidden_dims[0], hidden_dims[1],
                             beta=beta, threshold=threshold)
        self.fc3 = LinearLIF(hidden_dims[1], output_dim,
                             beta=beta, threshold=threshold)

    def forward(self, x):
        T, B, F = x.shape
        spk, mem_f1 = self.fc1(x[0])
        spk, mem_f2 = self.fc2(spk)
        spk, mem_f3 = self.fc3(spk)
        spk_rec = [spk]
        for t in range(1, T):
            spk, mem_f1 = self.fc1(x[t], mem_f1)
            spk, mem_f2 = self.fc2(spk, mem_f2)
            spk, mem_f3 = self.fc3(spk, mem_f3)
            spk_rec.append(spk)
        return torch.stack(spk_rec, dim=0)

    def decode(self, spikes):
        return spikes.mean(dim=0)

    def spike_rate(self, spikes):
        return spikes.mean()
