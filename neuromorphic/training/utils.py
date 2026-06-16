import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

class AverageMeter:
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0.0
        self.avg = 0.0
        self.sum = 0.0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

class EarlyStopping:
    def __init__(self, patience=10, min_delta=1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.best = float('inf')
        self.counter = 0
        self.stopped = False

    def __call__(self, val_loss):
        if val_loss < self.best - self.min_delta:
            self.best = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.stopped = True
        return self.stopped

def save_checkpoint(state, filename='checkpoint.pt'):
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    torch.save(state, filename)

def plot_training(train_losses, val_losses, spike_rates, filename='training_curve.png'):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(train_losses, label='Train')
    axes[0].plot(val_losses, label='Val')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True)
    axes[1].plot(spike_rates)
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Spike Rate')
    axes[1].grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=100)
    plt.close()
